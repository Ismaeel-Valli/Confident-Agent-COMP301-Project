import type { LMStudioClient } from '@lmstudio/sdk';
export function cosineSimilarity(vecA: number[], vecB: number[]): number {
  const dotProduct = vecA.reduce((acc, val, i) => acc + val * vecB[i], 0);
  const magA = Math.sqrt(vecA.reduce((acc, val) => acc + val * val, 0));
  const magB = Math.sqrt(vecB.reduce((acc, val) => acc + val * val, 0));
  if (magA === 0 || magB === 0) {
    return 0;
  }
  return dotProduct / (magA * magB);
}

// Main RAG-on-text helper
export async function performRagOnText(text: string, query: string, client: LMStudioClient, embeddingModelName: string) {
  // 1. Load embedding model
  const embeddingModel = await client.embedding.model(embeddingModelName);

  // 2. Chunk the text (simple paragraph-based chunking)
  const chunks = text.split(/\n\s*\n/).filter(chunk => chunk.trim().length > 20);
  if (chunks.length === 0) {
    return [{ chunk: text.substring(0, 4000), score: 1 }];
  }

  // 3. Embed query and chunks
  const [queryEmbedding] = await embeddingModel.embed([query]);
  const chunkEmbeddings = await embeddingModel.embed(chunks);

  // 4. Calculate similarity
  const similarities = chunkEmbeddings.map((chunkEmb, i) => ({
    chunk: chunks[i],
    score: cosineSimilarity(queryEmbedding.embedding, chunkEmb.embedding),
  }));

  // 5. Sort by score and return top results
  similarities.sort((a, b) => b.score - a.score);
  return similarities.slice(0, 5); // Return top 5
}


