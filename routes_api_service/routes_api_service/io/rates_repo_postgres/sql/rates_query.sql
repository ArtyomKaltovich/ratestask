with date_range as (
	SELECT generate_series($3::date, $4, '1 day')::date AS date_range
)
select to_char(date_range,'yyyy-mm-dd'), avg_price from date_range
left join (
	select day, avg(price) as avg_price
	from prices p
	where
		orig_code in (
			select slug from destinations d
			where is_port is true and path ~ $1
		)
		and dest_code in (
			select slug from destinations d
			where is_port is true and path ~ $2
		)
	group by day
	having count(price) >= 3
	) as day_prices
on date_range = day_prices.day
