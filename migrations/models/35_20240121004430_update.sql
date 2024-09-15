-- upgrade --
ALTER TABLE "achievement" ADD "rewards" TEXT;
ALTER TABLE "achievement" ADD "firstball" BOOLEAN DEFAULT FALSE;
-- downgrade --
ALTER TABLE "achievement" DROP COLUMN "rewards";
ALTER TABLE "achievement" DROP COLUMN "firstball";