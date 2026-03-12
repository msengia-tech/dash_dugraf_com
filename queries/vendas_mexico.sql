-- queries/vendas_mexico.sql
SELECT 
  codpro, codigo_cliente, nota_fiscal, empresa, filial, razao_social, cidade, uf,
  nome_representante, apelido_representante, emissao, ano, mes, produto, fabricante,
  familia, tipo, qtde, unimed, m2, total_r, ptax_data, ptax_negociado, ptax_valor,
  total_us, us_m2, novo_comum, novo_trelleborg, ramo_categoria
FROM vw_dashboard_comercial_mexico
WHERE emissao > '2017-01-01'
ORDER BY emissao;