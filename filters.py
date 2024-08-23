
def filter_PZ(title, summary, authors, published, link, category):

    IN_ASTRO =  'astro-ph.IM' in category or\
        'astro-ph.GA'  in category or\
        'astro-ph.CO' in category or\
        'astro-ph.HE'  in category

    IN_ML =  'cs.CV' in category or\
             'cs.AI' in category or\
             'stat.ML' in category

    IN_PHOTOZ =  'photometric redshift' in title.lower() or\
                 'photometric redshift' in summary.lower() or\
                 'photo-z' in title.lower() or\
                 'photo-z' in summary.lower()

    FILTER_RESULT = (IN_ASTRO or IN_ML) and IN_PHOTOZ
    return FILTER_RESULT

def filter_DG(title, summary, authors, published, link, category):

    IN_ASTRO =  'astro-ph.IM' in category or\
        'astro-ph.GA'  in category or\
        'astro-ph.CO' in category or\
        'astro-ph.HE'  in category

    IN_ML = 'cs.CV' in category or\
            'cs.AI' in category or\
            'stat.ML' in category

    IN_DWARF = 'dwarf galaxy' in title.lower() or\
               'dwarf galaxy' in summary.lower() or\
                'dwarf galaxies' in title.lower() or\
                'dwarf galaxies' in summary.lower()

    FILTER_RESULT = IN_ASTRO and IN_DWARF
    return FILTER_RESULT

def filter_authors(title, summary, authors, published, link, category):

    MY_AUTHORS = ['G. Narayan','A. Peters','C. Hirata']

    cross_match = [my_author in authors for my_author in MY_AUTHORS]
    
    FILTER_RESULT=False
    for value in cross_match: #if any of these pop true, its True.
        if value:
            FILTER_RESULT=True
        
    return FILTER_RESULT

__filters__ = [filter_PZ, filter_DG, filter_authors]

