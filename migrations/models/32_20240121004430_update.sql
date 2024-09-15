-- upgrade --
CREATE TABLE IF NOT EXISTS "achievement" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(48) UNIQUE NOT NULL,
    "requirements" TEXT,
    "achievable" BOOLEAN DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
);

CREATE TABLE IF NOT EXISTS "achievementinstance" (
    "id" SERIAL PRIMARY KEY,
    "achievement_id" INTEGER NOT NULL,
    "player_id" INT NOT NULL REFERENCES "player" ("id") ON DELETE CASCADE,
    "achieved_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "server_id" BIGINT,
    FOREIGN KEY ("achievement_id") REFERENCES "achievement" ("id") ON DELETE CASCADE,
    CONSTRAINT "unique_player_achievement" UNIQUE ("player_id", "achievement_id")
);
-- downgrade --
DROP TABLE IF EXISTS "achievement";
DROP TABLE IF EXISTS "achievementinstance";