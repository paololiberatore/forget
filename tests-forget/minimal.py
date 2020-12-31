analyze(
    'forgetting x maintains size unless variables are introduced',
    {'ab->x', 'xc->d', 'xc->e', 'xc->f'},
    {'a', 'b', 'c', 'd', 'e', 'f'}
)
