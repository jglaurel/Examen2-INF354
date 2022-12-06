declare		@cadena1 varchar(50),
			@cadena2 varchar(50),
			@len_cadena1 int,
			@len_cadena2 int,
			@contador int,
			@sql nvarchar(4000),
			@letra varchar(3),
			@columna varchar(10),
			@len_table int

set @cadena1='martha'
set @cadena2='martha'
set @len_cadena1=LEN(@cadena1)
set @len_cadena2=LEN(@cadena2)
set @contador=0
set @sql='create table nombre (';
while @contador<@len_cadena1
begin
	set @letra=LEFT(@cadena1,1)+cast(@contador as varchar(1))
	set @sql=@sql+@letra+' int,'
	set @cadena1 = RIGHT(@cadena1, LEN(@cadena1)-1)
	set @contador=@contador+1
end
set @sql=LEFT(@sql,LEN(@sql)-1)
set @sql=@sql+')'
print(@sql)
exec sp_executesql @sql
set @contador=0
while @contador<@len_cadena2
begin
	set @letra=LEFT(@cadena2,1)
	set @cadena2 = RIGHT(@cadena2, LEN(@cadena2)-1)
	select top 1 @columna=COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS
		where TABLE_NAME='nombre'
		and LEFT(COLUMN_NAME,1)=@letra
		and ORDINAL_POSITION>=@contador
	set @sql='insert into nombre('+@columna+') values(1)'
	exec sp_executesql @sql
	set @contador=@contador+1
end

set @contador=1
select @len_table=count(*) 
	from INFORMATION_SCHEMA.COLUMNS
	where TABLE_NAME='nombre'
set @sql=''
while @contador<=@len_table
begin
	select @columna=COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS
		where TABLE_NAME='nombre'
		and ORDINAL_POSITION=@contador
	set @sql=@sql+'sum('+@columna+'),'
	set @contador=@contador+1
end
set @sql='select '+LEFT(@sql, LEN(@sql)-1)
set @sql=@sql+' from nombre'
print (@sql)

select * from nombre

drop table nombre