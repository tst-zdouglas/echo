struct Meta {
  string k,
  i32 t,
  binary v
}

service Echo {
  list<Meta> echo(
    list<Meta> metas
  )
}
