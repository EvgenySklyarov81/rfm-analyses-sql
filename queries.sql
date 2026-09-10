-- ============================================================
-- RFM-анализ покупателей
-- ============================================================

-- ------------------------------------------------------------
-- Шаг 1. Проверка качества данных
-- Считаем количество и долю идентифицированных и неидентифицированных покупателей
-- ------------------------------------------------------------
select case when length(card) = 13 then 'identified' else 'not_identified' end as customer
     , count(*) as qty
     , to_char(round(count(*) / sum(count(*)) over() * 100), '99 %') as perc
  from bonuscheques
 group by customer;
-- ------------------------------------------------------------
-- Шаг 2. Финальный RFM-запрос
-- ------------------------------------------------------------
-- Рассчитывает R, F, M для каждого клиента, присваивает ранги
-- 1–3 по 33-му и 66-му процентилям и агрегирует результат
-- по RFM-группам.
-- ------------------------------------------------------------
with agg_data as(
select card as user_id
     , (select max(datetime)::date from bonuscheques) - max(datetime::date) as recency
     , count(datetime) as frequency
     , sum(summ_with_disc) as monetary
  from bonuscheques
 where length(card) = 13
 group by card
),
percentiles as(
select (percentile_cont(array[0.33, 0.66]) within group(order by recency))[1] as rec_perc_033
     , (percentile_cont(array[0.33, 0.66]) within group(order by recency))[2] as rec_perc_066
     , (percentile_cont(array[0.33, 0.66]) within group(order by frequency))[1] as freq_perc_033
     , (percentile_cont(array[0.33, 0.66]) within group(order by frequency))[2] as freq_perc_066
     , (percentile_cont(array[0.33, 0.66]) within group(order by monetary))[1] as monet_perc_033
     , (percentile_cont(array[0.33, 0.66]) within group(order by monetary))[2] as monet_perc_066
  from agg_data
),
rfm as(
select user_id
     , case when recency <= (select rec_perc_033 from percentiles) then '1'
            when recency <= (select rec_perc_066 from percentiles) then '2'
            else '3'
            end as recency   
     , case when frequency <= (select freq_perc_033 from percentiles) then '3'
            when frequency <= (select freq_perc_066 from percentiles) then '2'
            else '1'
            end as frequency
     , case when monetary <= (select monet_perc_033 from percentiles) then '3'
            when monetary <= (select monet_perc_066 from percentiles) then '2'  
            else '1'
            end as monetary            
  from agg_data
)
select recency || frequency || monetary as rfm_group
     , count(*) as customers
  from rfm
 group by 1
 order by rfm_group;
