"""
Memory Service Module

Manages chat memory and conversation history with size limits, cleanup,
and mathematical context preservation for enhanced learning experiences.

This module focuses on:
- Chat memory management with conversation history
- Memory size limits and automatic cleanup
- Conversation export/import functionality  
- Mathematical context preservation
- Conversation threading and organization
"""

import logging
import json
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import deque
import pickle

from src.core.config import ConfigManager

logger = logging.getLogger(__name__)

@dataclass
class ChatMessage:
    """Individual chat message structure"""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: float
    metadata: Dict[str, Any] = None
    mathematical_content: bool = False
    tokens_used: Optional[int] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.timestamp is None:
            self.timestamp = time.time()

@dataclass
class ConversationSession:
    """Conversation session structure"""
    session_id: str
    title: str
    created_at: float
    last_activity: float
    message_count: int
    total_tokens: int
    mathematical_focus: bool = False
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class MemoryServiceError(Exception):
    """Custom exception for memory service errors"""
    pass

class MemoryService:
    """
    Enhanced memory service for chat history and conversation management.
    
    Features:
    - Conversation history with mathematical context preservation
    - Automatic memory size management and cleanup
    - Session-based conversation organization
    - Export/import functionality for conversation backup
    - Mathematical content tagging and search
    - Token usage tracking and optimization
    """
    
    def __init__(self, config: ConfigManager):
        """
        Initialize memory service with configuration.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        
        # Memory configuration
        self.max_messages = self.config.get("memory.max_messages", 1000)
        self.max_sessions = self.config.get("memory.max_sessions", 50)
        self.max_message_age_days = self.config.get("memory.max_message_age_days", 30)
        self.cleanup_interval = self.config.get("memory.cleanup_interval", 3600)  # 1 hour
        
        # Storage configuration
        self.storage_dir = Path(self.config.get("memory.storage_dir", "data/memory"))
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory storage
        self.sessions: Dict[str, ConversationSession] = {}
        self.messages: Dict[str, deque] = {}  # session_id -> deque of messages
        self.current_session_id: Optional[str] = None
        
        # Cleanup tracking
        self.last_cleanup = time.time()
        
        # Load existing sessions
        self._load_sessions()
        
        logger.info("Memory service initialized", extra={
            "max_messages": self.max_messages,
            "max_sessions": self.max_sessions,
            "storage_dir": str(self.storage_dir),
            "loaded_sessions": len(self.sessions)
        })
    
    def create_session(
        self, 
        title: str = None, 
        mathematical_focus: bool = False
    ) -> str:
        """
        Create a new conversation session.
        
        Args:
            title: Optional session title
            mathematical_focus: Whether session focuses on mathematical content
            
        Returns:
            str: Session ID
        """
        session_id = f"session_{int(time.time() * 1000)}"
        
        if title is None:
            title = f"Conversation {len(self.sessions) + 1}"
        
        session = ConversationSession(
            session_id=session_id,
            title=title,
            created_at=time.time(),
            last_activity=time.time(),
            message_count=0,
            total_tokens=0,
            mathematical_focus=mathematical_focus
        )
        
        self.sessions[session_id] = session
        self.messages[session_id] = deque(maxlen=self.max_messages)
        self.current_session_id = session_id
        
        # Clean up old sessions if needed
        self._cleanup_old_sessions()
        
        logger.info(
            "New conversation session created",
            extra={
                "session_id": session_id,
                "title": title,
                "mathematical_focus": mathematical_focus
            }
        )
        
        return session_id
    
    def switch_session(self, session_id: str) -> bool:
        """
        Switch to an existing session.
        
        Args:
            session_id: Target session ID
            
        Returns:
            bool: True if switch successful
        """
        if session_id not in self.sessions:
            logger.error("Session not found", extra={"session_id": session_id})
            return False
        
        old_session = self.current_session_id
        self.current_session_id = session_id
        
        # Update last activity
        self.sessions[session_id].last_activity = time.time()
        
        logger.info(
            "Switched conversation session",
            extra={"from": old_session, "to": session_id}
        )
        
        return True
    
    def add_message(
        self, 
        role: str, 
        content: str, 
        mathematical_content: bool = False,
        tokens_used: Optional[int] = None,
        metadata: Dict[str, Any] = None
    ) -> None:
        """
        Add a message to the current session.
        
        Args:
            role: Message role ('user', 'assistant', 'system')
            content: Message content
            mathematical_content: Whether message contains mathematical content
            tokens_used: Number of tokens used for this message
            metadata: Additional metadata
        """
        if not self.current_session_id:
            # Create default session
            self.create_session("Default Conversation")
        
        message = ChatMessage(
            role=role,
            content=content,
            timestamp=time.time(),
            mathematical_content=mathematical_content,
            tokens_used=tokens_used,
            metadata=metadata or {}
        )
        
        # Add to current session
        self.messages[self.current_session_id].append(message)
        
        # Update session metadata
        session = self.sessions[self.current_session_id]
        session.message_count += 1
        session.last_activity = time.time()
        
        if tokens_used:
            session.total_tokens += tokens_used
        
        if mathematical_content:
            session.mathematical_focus = True
            if "mathematical" not in session.tags:
                session.tags.append("mathematical")
        
        logger.debug(
            "Message added to session",
            extra={
                "session_id": self.current_session_id,
                "role": role,
                "mathematical_content": mathematical_content,
                "tokens_used": tokens_used
            }
        )
        
        # Periodic cleanup check
        if time.time() - self.last_cleanup > self.cleanup_interval:
            self._cleanup_old_messages()
    
    def get_recent_messages(
        self, 
        limit: int = 10,
        session_id: Optional[str] = None,
        include_system: bool = False
    ) -> List[ChatMessage]:
        """
        Get recent messages from specified or current session.
        
        Args:
            limit: Maximum number of messages to return
            session_id: Optional specific session ID
            include_system: Whether to include system messages
            
        Returns:
            List[ChatMessage]: List of recent messages
        """
        target_session = session_id or self.current_session_id
        
        if not target_session or target_session not in self.messages:
            return []
        
        messages = list(self.messages[target_session])
        
        if not include_system:
            messages = [m for m in messages if m.role != 'system']
        
        # Return most recent messages
        return messages[-limit:] if messages else []
    
    def get_conversation_context(
        self, 
        max_tokens: int = 4000,
        session_id: Optional[str] = None
    ) -> str:
        """
        Get conversation context optimized for token limits.
        
        Args:
            max_tokens: Maximum tokens to include in context
            session_id: Optional specific session ID
            
        Returns:
            str: Formatted conversation context
        """
        target_session = session_id or self.current_session_id
        
        if not target_session or target_session not in self.messages:
            return ""
        
        messages = list(self.messages[target_session])
        context_parts = []
        estimated_tokens = 0
        
        # Work backwards from most recent messages
        for message in reversed(messages):
            if message.role == 'system':
                continue
            
            # Rough token estimation (4 chars per token)
            message_tokens = len(message.content) // 4
            
            if estimated_tokens + message_tokens > max_tokens:
                break
            
            context_parts.append(f"{message.role.title()}: {message.content}")
            estimated_tokens += message_tokens
        
        # Reverse to get chronological order
        context_parts.reverse()
        
        return "\n\n".join(context_parts) if context_parts else ""
    
    def search_messages(
        self, 
        query: str, 
        mathematical_only: bool = False,
        session_id: Optional[str] = None
    ) -> List[Tuple[str, ChatMessage]]:
        """
        Search messages across sessions.
        
        Args:
            query: Search query
            mathematical_only: Only search mathematical content
            session_id: Optional specific session to search
            
        Returns:
            List[Tuple[str, ChatMessage]]: List of (session_id, message) pairs
        """
        results = []
        query_lower = query.lower()
        
        # Determine sessions to search
        if session_id:
            search_sessions = [session_id] if session_id in self.messages else []
        else:
            search_sessions = list(self.messages.keys())
        
        for sid in search_sessions:
            for message in self.messages[sid]:
                # Skip if looking for mathematical content only
                if mathematical_only and not message.mathematical_content:
                    continue
                
                # Simple text search
                if query_lower in message.content.lower():
                    results.append((sid, message))
        
        # Sort by timestamp (most recent first)
        results.sort(key=lambda x: x[1].timestamp, reverse=True)
        
        return results
    
    def get_session_statistics(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics for a session.
        
        Args:
            session_id: Optional specific session ID
            
        Returns:
            Dict[str, Any]: Session statistics
        """
        target_session = session_id or self.current_session_id
        
        if not target_session or target_session not in self.sessions:
            return {}
        
        session = self.sessions[target_session]
        messages = list(self.messages[target_session])
        
        # Calculate statistics
        user_messages = [m for m in messages if m.role == 'user']
        assistant_messages = [m for m in messages if m.role == 'assistant']
        mathematical_messages = [m for m in messages if m.mathematical_content]
        
        total_chars = sum(len(m.content) for m in messages)
        avg_message_length = total_chars / len(messages) if messages else 0
        
        return {
            "session_id": target_session,
            "title": session.title,
            "created_at": session.created_at,
            "last_activity": session.last_activity,
            "duration_hours": (session.last_activity - session.created_at) / 3600,
            "total_messages": len(messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "mathematical_messages": len(mathematical_messages),
            "total_tokens": session.total_tokens,
            "total_characters": total_chars,
            "avg_message_length": avg_message_length,
            "mathematical_focus": session.mathematical_focus,
            "tags": session.tags
        }
    
    def export_session(self, session_id: str, file_path: Path = None) -> Optional[Path]:
        """
        Export session to file.
        
        Args:
            session_id: Session ID to export
            file_path: Optional custom export path
            
        Returns:
            Path: Export file path if successful
        """
        if session_id not in self.sessions:
            logger.error("Session not found for export", extra={"session_id": session_id})
            return None
        
        if file_path is None:
            export_dir = self.storage_dir / "exports"
            export_dir.mkdir(exist_ok=True)
            file_path = export_dir / f"{session_id}_{int(time.time())}.json"
        
        try:
            session_data = {
                "session": asdict(self.sessions[session_id]),
                "messages": [asdict(msg) for msg in self.messages[session_id]]
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            logger.info(
                "Session exported successfully",
                extra={"session_id": session_id, "file_path": str(file_path)}
            )
            
            return file_path
            
        except Exception as e:
            logger.error("Error exporting session", extra={"error": str(e), "session_id": session_id})
            return None
    
    def import_session(self, file_path: Path) -> Optional[str]:
        """
        Import session from file.
        
        Args:
            file_path: Path to import file
            
        Returns:
            str: Imported session ID if successful
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            # Reconstruct session
            session_dict = session_data["session"]
            session = ConversationSession(**session_dict)
            
            # Generate new session ID if it already exists
            original_id = session.session_id
            counter = 1
            while session.session_id in self.sessions:
                session.session_id = f"{original_id}_imported_{counter}"
                counter += 1
            
            # Reconstruct messages
            messages = deque(maxlen=self.max_messages)
            for msg_dict in session_data["messages"]:
                message = ChatMessage(**msg_dict)
                messages.append(message)
            
            # Store imported session
            self.sessions[session.session_id] = session
            self.messages[session.session_id] = messages
            
            logger.info(
                "Session imported successfully",
                extra={"session_id": session.session_id, "file_path": str(file_path)}
            )
            
            return session.session_id
            
        except Exception as e:
            logger.error("Error importing session", extra={"error": str(e), "file_path": str(file_path)})
            return None
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session and its messages.
        
        Args:
            session_id: Session ID to delete
            
        Returns:
            bool: True if deletion successful
        """
        if session_id not in self.sessions:
            logger.error("Session not found for deletion", extra={"session_id": session_id})
            return False
        
        # Remove from memory
        del self.sessions[session_id]
        del self.messages[session_id]
        
        # Switch to another session if this was current
        if self.current_session_id == session_id:
            if self.sessions:
                self.current_session_id = next(iter(self.sessions.keys()))
            else:
                self.current_session_id = None
        
        logger.info("Session deleted", extra={"session_id": session_id})
        return True
    
    def get_all_sessions(self) -> List[ConversationSession]:
        """
        Get list of all sessions sorted by last activity.
        
        Returns:
            List[ConversationSession]: List of sessions
        """
        sessions = list(self.sessions.values())
        sessions.sort(key=lambda s: s.last_activity, reverse=True)
        return sessions
    
    def clear_session(self, session_id: Optional[str] = None) -> bool:
        """
        Clear messages from a session.
        
        Args:
            session_id: Optional specific session ID
            
        Returns:
            bool: True if clearing successful
        """
        target_session = session_id or self.current_session_id
        
        if not target_session or target_session not in self.messages:
            return False
        
        self.messages[target_session].clear()
        
        # Reset session statistics
        session = self.sessions[target_session]
        session.message_count = 0
        session.total_tokens = 0
        session.last_activity = time.time()
        
        logger.info("Session messages cleared", extra={"session_id": target_session})
        return True
    
    def _cleanup_old_sessions(self) -> None:
        """Remove old sessions if exceeding maximum"""
        if len(self.sessions) <= self.max_sessions:
            return
        
        # Sort by last activity (oldest first)
        sessions_by_activity = sorted(
            self.sessions.items(),
            key=lambda x: x[1].last_activity
        )
        
        # Remove oldest sessions
        sessions_to_remove = len(self.sessions) - self.max_sessions
        for i in range(sessions_to_remove):
            session_id, _ = sessions_by_activity[i]
            if session_id != self.current_session_id:  # Don't remove current session
                self.delete_session(session_id)
                logger.info("Removed old session", extra={"session_id": session_id})
    
    def _cleanup_old_messages(self) -> None:
        """Remove old messages based on age"""
        current_time = time.time()
        cutoff_time = current_time - (self.max_message_age_days * 24 * 3600)
        
        for session_id, messages in self.messages.items():
            original_count = len(messages)
            
            # Filter out old messages
            recent_messages = deque(
                [m for m in messages if m.timestamp > cutoff_time],
                maxlen=self.max_messages
            )
            
            if len(recent_messages) < original_count:
                self.messages[session_id] = recent_messages
                removed_count = original_count - len(recent_messages)
                
                # Update session count
                self.sessions[session_id].message_count = len(recent_messages)
                
                logger.info(
                    "Cleaned up old messages",
                    extra={"session_id": session_id, "removed_count": removed_count}
                )
        
        self.last_cleanup = current_time
    
    def _save_sessions(self) -> None:
        """Save sessions to persistent storage"""
        try:
            sessions_file = self.storage_dir / "sessions.pkl"
            messages_file = self.storage_dir / "messages.pkl"
            
            # Save sessions metadata
            with open(sessions_file, 'wb') as f:
                pickle.dump(self.sessions, f)
            
            # Save messages (convert deques to lists for serialization)
            serializable_messages = {
                sid: list(messages) for sid, messages in self.messages.items()
            }
            with open(messages_file, 'wb') as f:
                pickle.dump(serializable_messages, f)
                
        except Exception as e:
            logger.error("Error saving sessions", extra={"error": str(e)})
    
    def _load_sessions(self) -> None:
        """Load sessions from persistent storage"""
        try:
            sessions_file = self.storage_dir / "sessions.pkl"
            messages_file = self.storage_dir / "messages.pkl"
            
            if sessions_file.exists() and messages_file.exists():
                # Load sessions metadata
                with open(sessions_file, 'rb') as f:
                    self.sessions = pickle.load(f)
                
                # Load messages (convert lists back to deques)
                with open(messages_file, 'rb') as f:
                    loaded_messages = pickle.load(f)
                    self.messages = {
                        sid: deque(messages, maxlen=self.max_messages)
                        for sid, messages in loaded_messages.items()
                    }
                
                # Set current session to most recent
                if self.sessions:
                    most_recent = max(self.sessions.values(), key=lambda s: s.last_activity)
                    self.current_session_id = most_recent.session_id
                
                logger.info("Sessions loaded from storage", extra={"session_count": len(self.sessions)})
                
        except Exception as e:
            logger.error("Error loading sessions", extra={"error": str(e)})
            # Initialize empty storage
            self.sessions = {}
            self.messages = {}
            self.current_session_id = None
    
    def __del__(self):
        """Save sessions on cleanup"""
        try:
            self._save_sessions()
        except Exception:
            pass  # Ignore errors during cleanup

    def add_user_message(self, content: str, **kwargs) -> None:
        """
        Convenience method to add a user message.
        
        Args:
            content: Message content
            **kwargs: Additional metadata
        """
        self.add_message("user", content, **kwargs)
    
    def add_ai_message(self, content: str, **kwargs) -> None:
        """
        Convenience method to add an AI assistant message.
        
        Args:
            content: Message content
            **kwargs: Additional metadata
        """
        self.add_message("assistant", content, **kwargs)
    
    def get_messages(self, session_id: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Get messages in a format compatible with LLM APIs.
        
        Args:
            session_id: Optional session ID (uses current session if None)
            
        Returns:
            List[Dict[str, str]]: Messages in LLM API format
        """
        recent_messages = self.get_recent_messages(session_id=session_id)
        return [
            {"role": msg.role, "content": msg.content}
            for msg in recent_messages
        ] 