create table requests (
  id bigint generated always as identity primary key,
  user_id bigint not null,
  full_name text,
  username text,
  created_at timestamptz default now()
);
