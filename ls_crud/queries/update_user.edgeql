select (
    update User filter .name = <str>$currrent_name
        set {name := <str>$new_name}
        )
        {name, created_at};