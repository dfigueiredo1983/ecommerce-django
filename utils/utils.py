def formata_preco(val):
    print('Valor formata_preco: ', val)
    return f'R$ {val:.2f}'.replace('.', ',')

def cart_total_qtde(carrinho):
    quantidade = sum([item['quantidade'] for item in carrinho.values()])
    return quantidade

def cart_total_valor(carrinho):
    return sum([item.get('quantidade') * item.get('preco_unitario_promocional') 
        for item 
        in carrinho.values()])
