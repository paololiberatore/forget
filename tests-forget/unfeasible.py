analyze(
    'replacing by d is unfeasible, only leads to forgotten variables',
    {'f->d', 'e->d', 'd->b', 'c->b', 'b->a'},
    {'c', 'a'}
)
