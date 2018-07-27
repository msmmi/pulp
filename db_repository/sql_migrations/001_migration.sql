-- auto-migrations didn't auto-generate defaults for the columns
ALTER TABLE "user" ALTER COLUMN admin SET DEFAULT FALSE;
ALTER TABLE "user" ALTER COLUMN liquid_cash SET DEFAULT 0;
ALTER TABLE "user" ALTER COLUMN cash_in_play SET DEFAULT 0;
ALTER TABLE "user" ALTER COLUMN created_at SET DEFAULT (now() at time zone 'utc');

ALTER TABLE wager ALTER COLUMN "group" SET DEFAULT FALSE;
ALTER TABLE wager ALTER COLUMN activated SET DEFAULT FALSE;
ALTER TABLE wager ALTER COLUMN created_at SET DEFAULT (now() at time zone 'utc');

ALTER TABLE taken_wager ALTER COLUMN created_at SET DEFAULT (now() at time zone 'utc');

ALTER TABLE result ALTER COLUMN created_at SET DEFAULT (now() at time zone 'utc');
