import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export async function cleanUpTokens() {
  const now = new Date();

  const deleted = await prisma.refreshToken.deleteMany({
    where: {
      OR: [{ valid: false }, { expiresAt: { lt: now } }],
    },
  });

  console.log(
    `[${new Date().toISOString()}] Deleted ${deleted.count} tokens.`
  );
}
