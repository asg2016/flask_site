drop table if exists 'goods';
create table goods (
  id integer primary key autoincrement,
  title text not null,
  description text null,
  cpu text not null,
  cpu_freq text not null,
  ram text not null,
  hdd text not null,
  display text not null,
  videocard text not null,
  weight real not null,
  dvd integer not null,
  lte integer not null,
  blutooth integer not null,
  wifi integer not null,
  colors text not null,
  images text not null,
  price real no null
);