-- upgrade --
ALTER TABLE "achievement" ADD "simplified_req" VARCHAR(48);
-- downgrade --
ALTER TABLE "achievement" DROP COLUMN "simplified_req";