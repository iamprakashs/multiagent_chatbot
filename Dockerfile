# Simple Qdrant Dockerfile
FROM qdrant/qdrant:latest

# Expose ports
EXPOSE 6333 6334

# Set environment variables
ENV QDRANT__SERVICE__HTTP_PORT=6333
ENV QDRANT__SERVICE__GRPC_PORT=6334

# Create storage directory
VOLUME ["/qdrant/storage"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:6333/health || exit 1

# Default command
CMD ["./qdrant"]