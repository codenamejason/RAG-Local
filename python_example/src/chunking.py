"""Document chunking utilities for RAG."""

from typing import List, Dict, Any, Optional
import re
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Chunk:
    """Represents a document chunk."""
    text: str
    metadata: Dict[str, Any]
    chunk_id: int
    source_doc_id: Optional[str] = None


class TextChunker:
    """Text chunking utility with various strategies."""
    
    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        separator: str = "\n\n"
    ):
        """
        Initialize text chunker.
        
        Args:
            chunk_size: Maximum size of each chunk in characters.
            chunk_overlap: Number of characters to overlap between chunks.
            separator: Primary separator for splitting text.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
        
        # Hierarchy of separators to try
        self.separators = [
            "\n\n",  # Paragraphs
            "\n",    # Lines
            ". ",    # Sentences
            ", ",    # Clauses
            " ",     # Words
            ""       # Characters
        ]
    
    def chunk_text(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Chunk]:
        """
        Chunk a text document.
        
        Args:
            text: Text to chunk.
            metadata: Optional metadata to attach to chunks.
            
        Returns:
            List of Chunk objects.
        """
        if not text:
            return []
        
        metadata = metadata or {}
        chunks = self._recursive_chunk(text)
        
        # Create Chunk objects
        chunk_objects = []
        for i, chunk_text in enumerate(chunks):
            chunk = Chunk(
                text=chunk_text,
                metadata={
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "chunk_size": len(chunk_text)
                },
                chunk_id=i
            )
            chunk_objects.append(chunk)
        
        logger.debug(f"Created {len(chunk_objects)} chunks from text")
        return chunk_objects
    
    def _recursive_chunk(self, text: str) -> List[str]:
        """
        Recursively chunk text using separators.
        
        Args:
            text: Text to chunk.
            
        Returns:
            List of text chunks.
        """
        chunks = []
        current_chunk = ""
        
        # Try to split by the primary separator first
        splits = text.split(self.separator)
        
        for split in splits:
            # If adding this split would exceed chunk size
            if len(current_chunk) + len(split) + len(self.separator) > self.chunk_size:
                # Save current chunk if it has content
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # If the split itself is too large, recursively chunk it
                if len(split) > self.chunk_size:
                    sub_chunks = self._split_large_text(split)
                    chunks.extend(sub_chunks)
                    current_chunk = ""
                else:
                    current_chunk = split
            else:
                # Add to current chunk
                if current_chunk:
                    current_chunk += self.separator + split
                else:
                    current_chunk = split
        
        # Don't forget the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Apply overlap
        if self.chunk_overlap > 0:
            chunks = self._apply_overlap(chunks)
        
        return chunks
    
    def _split_large_text(self, text: str) -> List[str]:
        """
        Split text that's larger than chunk_size.
        
        Args:
            text: Large text to split.
            
        Returns:
            List of chunks.
        """
        chunks = []
        
        # Try different separators
        for separator in self.separators[1:]:  # Skip the primary separator
            if separator:
                parts = text.split(separator)
                current = ""
                
                for part in parts:
                    if len(current) + len(part) + len(separator) <= self.chunk_size:
                        current += (separator if current else "") + part
                    else:
                        if current:
                            chunks.append(current)
                        current = part
                
                if current:
                    chunks.append(current)
                
                # If we successfully chunked, return
                if all(len(c) <= self.chunk_size for c in chunks):
                    return chunks
        
        # Last resort: split by character count
        for i in range(0, len(text), self.chunk_size):
            chunks.append(text[i:i + self.chunk_size])
        
        return chunks
    
    def _apply_overlap(self, chunks: List[str]) -> List[str]:
        """
        Apply overlap between chunks.
        
        Args:
            chunks: List of text chunks.
            
        Returns:
            List of chunks with overlap.
        """
        if len(chunks) <= 1:
            return chunks
        
        overlapped_chunks = []
        
        for i, chunk in enumerate(chunks):
            if i == 0:
                # First chunk: add overlap from next chunk
                if i + 1 < len(chunks):
                    next_chunk = chunks[i + 1]
                    overlap = next_chunk[:self.chunk_overlap]
                    overlapped_chunks.append(chunk + " " + overlap)
                else:
                    overlapped_chunks.append(chunk)
            elif i == len(chunks) - 1:
                # Last chunk: add overlap from previous chunk
                prev_chunk = chunks[i - 1]
                overlap = prev_chunk[-self.chunk_overlap:]
                overlapped_chunks.append(overlap + " " + chunk)
            else:
                # Middle chunks: add overlap from both sides
                prev_chunk = chunks[i - 1]
                next_chunk = chunks[i + 1]
                prev_overlap = prev_chunk[-self.chunk_overlap//2:]
                next_overlap = next_chunk[:self.chunk_overlap//2]
                overlapped_chunks.append(prev_overlap + " " + chunk + " " + next_overlap)
        
        return overlapped_chunks


class MarkdownChunker(TextChunker):
    """Specialized chunker for Markdown documents."""
    
    def chunk_text(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Chunk]:
        """
        Chunk markdown text, respecting heading structure.
        
        Args:
            text: Markdown text to chunk.
            metadata: Optional metadata.
            
        Returns:
            List of Chunk objects.
        """
        metadata = metadata or {}
        
        # Split by headers while preserving them
        header_pattern = r'^(#{1,6})\s+(.*)$'
        lines = text.split('\n')
        
        sections = []
        current_section = {
            'header': '',
            'level': 0,
            'content': []
        }
        
        for line in lines:
            header_match = re.match(header_pattern, line)
            
            if header_match:
                # Save current section if it has content
                if current_section['content']:
                    sections.append(current_section)
                
                # Start new section
                level = len(header_match.group(1))
                header = header_match.group(2)
                current_section = {
                    'header': header,
                    'level': level,
                    'content': [line]
                }
            else:
                current_section['content'].append(line)
        
        # Don't forget the last section
        if current_section['content']:
            sections.append(current_section)
        
        # Convert sections to chunks
        chunks = []
        for i, section in enumerate(sections):
            section_text = '\n'.join(section['content'])
            section_metadata = {
                **metadata,
                'section_header': section['header'],
                'section_level': section['level'],
                'section_index': i
            }
            
            # If section is too large, use parent chunking
            if len(section_text) > self.chunk_size:
                sub_chunks = super().chunk_text(section_text, section_metadata)
                chunks.extend(sub_chunks)
            else:
                chunk = Chunk(
                    text=section_text,
                    metadata=section_metadata,
                    chunk_id=len(chunks)
                )
                chunks.append(chunk)
        
        return chunks
