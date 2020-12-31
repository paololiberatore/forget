analyze(
   'exponentially many branches, but only a resulting clauses',
   {'k->a', 'k->b', 'l->d', 'l->e', 'm->g', 'm->h',
    'a->c', 'b->c', 'd->f', 'e->f', 'g->i', 'h->i',
    'cfi->j'},
   {'k', 'l', 'm', 'j'}
)
