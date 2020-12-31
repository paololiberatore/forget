analyze(
   'not single-head, but equivalent to one (the next)',
   {'a->b', 'b->c', 'c->d', 'd->e', 'e->f',
    'a->c', 'b->d', 'c->e', 'd->f'},
   {'a', 'f'}
)

analyze(
   'single-head, equivalent to the previous',
   {'a->b', 'b->c', 'c->d', 'd->e', 'e->f'},
   {'a', 'f'}
)
