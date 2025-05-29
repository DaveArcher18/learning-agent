"""
Document loading and chunking service.

This service handles loading documents from the data/documents directory,
implementing intelligent chunking that preserves mathematical content integrity
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from ..observability.logger import get_logger
from ..core.config import ConfigManager

logger = get_logger(__name__)


@dataclass
class DocumentChunk:
    """A chunk of document content with metadata."""
    content: str
    source_file: str
    chunk_index: int
    total_chunks: int
    start_char: int
    end_char: int


@dataclass
class DocumentInfo:
    """Information about a loaded document."""
    file_path: str
    file_name: str
    content: str
    size_bytes: int
    chunks: List[DocumentChunk]


class DocumentService:
    """
    Service for loading and chunking documents.
    
    Handles full document loading with intelligent chunking that preserves
    mathematical notation and context boundaries.
    """
    
    def __init__(self, config: ConfigManager):
        """
        Initialize the document service.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        
        # Get document configuration from config.yaml
        doc_config = config.get('documents', {})
        self.documents_dir = Path(doc_config.get('path', 'data/documents'))
        self.chunk_size = doc_config.get('chunk_size', 4000)
        self.chunk_overlap = doc_config.get('chunk_overlap', 500)
        self.preserve_boundaries = doc_config.get('preserve_boundaries', True)
        
        logger.info(f"DocumentService initialized with path: {self.documents_dir}")
        logger.info(f"Chunk size: {self.chunk_size} tokens, overlap: {self.chunk_overlap} tokens")
    
    def load_all_documents(self) -> List[DocumentInfo]:
        """
        Load all documents from the documents directory.
        
        Returns:
            List of DocumentInfo objects
        """
        logger.info("Loading all documents from directory")
        
        if not self.documents_dir.exists():
            logger.warning(f"Documents directory does not exist: {self.documents_dir}")
            return []
        
        documents = []
        
        for file_path in self.documents_dir.glob("*.md"):
            try:
                doc_info = self._load_document(file_path)
                if doc_info:
                    documents.append(doc_info)
                    logger.info(f"Loaded document: {file_path.name} ({doc_info.size_bytes} bytes, {len(doc_info.chunks)} chunks)")
            except Exception as e:
                logger.error(f"Failed to load document {file_path}: {e}")
        
        logger.info(f"Successfully loaded {len(documents)} documents")
        return documents
    
    def _load_document(self, file_path: Path) -> Optional[DocumentInfo]:
        """
        Load a single document and create chunks.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            DocumentInfo object or None if loading failed
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            size_bytes = len(content.encode('utf-8'))
            
            # Create chunks
            chunks = self._create_chunks(content, file_path.name)
            
            return DocumentInfo(
                file_path=str(file_path),
                file_name=file_path.name,
                content=content,
                size_bytes=size_bytes,
                chunks=chunks
            )
            
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {e}")
            return None
    
    def _create_chunks(self, content: str, file_name: str) -> List[DocumentChunk]:
        """
        Create intelligent chunks from document content.
        
        Args:
            content: Full document content
            file_name: Name of the source file
            
        Returns:
            List of DocumentChunk objects
        """
        if len(content) <= self.chunk_size:
            # Document is small enough to be a single chunk
            return [DocumentChunk(
                content=content,
                source_file=file_name,
                chunk_index=0,
                total_chunks=1,
                start_char=0,
                end_char=len(content)
            )]
        
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(content):
            end = min(start + self.chunk_size, len(content))
            
            # If we're not at the end and preserve_boundaries is enabled,
            # try to find a good break point
            if end < len(content) and self.preserve_boundaries:
                end = self._find_chunk_boundary(content, start, end)
            
            chunk_content = content[start:end]
            
            # Add overlap from previous chunk if not the first chunk
            if chunk_index > 0 and self.chunk_overlap > 0:
                overlap_start = max(0, start - self.chunk_overlap)
                overlap_content = content[overlap_start:start]
                chunk_content = overlap_content + chunk_content
            
            chunks.append(DocumentChunk(
                content=chunk_content,
                source_file=file_name,
                chunk_index=chunk_index,
                total_chunks=0,  # Will be updated after all chunks are created
                start_char=start,
                end_char=end
            ))
            
            start = end
            chunk_index += 1
        
        # Update total_chunks for all chunks
        for chunk in chunks:
            chunk.total_chunks = len(chunks)
        
        return chunks
    
    def _find_chunk_boundary(self, content: str, start: int, end: int) -> int:
        """
        Find a good boundary for chunking that preserves context.
        
        Args:
            content: Full document content
            start: Start position of chunk
            end: Initial end position of chunk
            
        Returns:
            Adjusted end position
        """
        # Look for good break points in order of preference
        search_back = min(200, end - start - 100)  # Don't search too far back
        search_start = end - search_back
        
        # 1. Try to break at paragraph boundaries (double newline)
        paragraph_match = content.rfind('\n\n', search_start, end)
        if paragraph_match > search_start:
            return paragraph_match + 2
        
        # 2. Try to break at section headers
        header_pattern = r'\n#{1,6}\s'
        for match in re.finditer(header_pattern, content[search_start:end]):
            pos = search_start + match.start()
            if pos > search_start:
                return pos + 1
        
        # 3. Try to break at end of sentences
        sentence_pattern = r'[.!?]\s+'
        for match in re.finditer(sentence_pattern, content[search_start:end]):
            pos = search_start + match.end()
            if pos > search_start:
                return pos
        
        # 4. Try to break at newlines
        newline_pos = content.rfind('\n', search_start, end)
        if newline_pos > search_start:
            return newline_pos + 1
        
        # 5. Fallback: break at word boundaries
        word_pattern = r'\s+'
        for match in re.finditer(word_pattern, content[search_start:end]):
            pos = search_start + match.start()
            if pos > search_start:
                return pos
        
        # If no good boundary found, use original end
        return end
    
    def get_document_summary(self) -> Dict[str, Any]:
        """
        Get a summary of loaded documents.
        
        Returns:
            Dictionary with document statistics
        """
        documents = self.load_all_documents()
        
        total_size = sum(doc.size_bytes for doc in documents)
        total_chunks = sum(len(doc.chunks) for doc in documents)
        
        return {
            'total_documents': len(documents),
            'total_size_bytes': total_size,
            'total_chunks': total_chunks,
            'average_chunk_size': total_chunks // len(documents) if documents else 0,
            'documents': [
                {
                    'name': doc.file_name,
                    'size_bytes': doc.size_bytes,
                    'chunks': len(doc.chunks)
                }
                for doc in documents
            ]
        }
    
    def get_all_chunks(self) -> List[DocumentChunk]:
        """
        Get all chunks from all documents.
        
        Returns:
            List of all DocumentChunk objects
        """
        documents = self.load_all_documents()
        all_chunks = []
        
        for doc in documents:
            all_chunks.extend(doc.chunks)
        
        return all_chunks
    
    def search_chunks(self, query: str, max_chunks: int = 5) -> List[DocumentChunk]:
        """
        Simple text-based search through chunks.
        
        Args:
            query: Search query
            max_chunks: Maximum number of chunks to return
            
        Returns:
            List of relevant DocumentChunk objects
        """
        all_chunks = self.get_all_chunks()
        query_lower = query.lower()
        
        # Score chunks by keyword overlap
        scored_chunks = []
        for chunk in all_chunks:
            content_lower = chunk.content.lower()
            score = sum(1 for word in query_lower.split() if word in content_lower)
            if score > 0:
                scored_chunks.append((score, chunk))
        
        # Sort by score and return top chunks
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk for _, chunk in scored_chunks[:max_chunks]] 