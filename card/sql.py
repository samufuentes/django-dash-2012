# Query for free text searching in the hstore
CARD_SEARCH_QUERY = '''
select id from (
    select id, sum(match) as matches
    from (
        select id,
            case when needle = haystack OR needleb = haystackb then 1
                else 0
            end as match
        from (
            select id, 
                dmetaphone(unnest) as needle,  
                dmetaphone(word) as haystack,
                dmetaphone_alt(unnest) as needleb,
                dmetaphone_alt(word) as haystackb
            from unnest(%s), (
                select id, 
                    unnest(string_to_array(_data->'name', ' ')) as word
                from card_card
            ) first
        ) second
    ) third group by id
) final
where matches >= %s 
order by matches desc;
'''
