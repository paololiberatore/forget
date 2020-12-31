analyze(
    'replacing by d is unfeasible: loop of forgotten variables e,f',
    {'e->f', 'f->e', 'e->d', 'd->b', 'c->b', 'b->a'},
    {'c', 'a'}
)
