-- auto-migrations didn't auto-generate defaults for the columns
ALTER TABLE "user" ALTER COLUMN admin SET DEFAULT FALSE;
ALTER TABLE "user" ALTER COLUMN liquid_cash SET DEFAULT 0;
ALTER TABLE "user" ALTER COLUMN cash_in_play SET DEFAULT 0;
ALTER TABLE "user" ALTER COLUMN created_at SET DEFAULT (now() at time zone 'utc');

ALTER TABLE event ALTER COLUMN line SET DEFAULT 0;
ALTER TABLE event ALTER COLUMN event_over SET DEFAULT FALSE;
ALTER TABLE event ALTER COLUMN created_at SET DEFAULT (now() at time zone 'utc');

ALTER TABLE wager ALTER COLUMN line SET DEFAULT 0;
ALTER TABLE wager ALTER COLUMN created_at SET DEFAULT (now() at time zone 'utc');

ALTER TABLE taken_wager ALTER COLUMN created_at SET DEFAULT (now() at time zone 'utc');

ALTER TABLE matched_wager ALTER COLUMN created_at SET DEFAULT (now() at time zone 'utc');

ALTER TABLE result ALTER COLUMN created_at SET DEFAULT (now() at time zone 'utc');
ALTER TABLE result ALTER COLUMN wager_result SET DEFAULT 0;
