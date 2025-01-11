def formata_preco(val):
    print('Val: ', val)
    return f'R$ {val:.2f}'.replace('.', ',')

def cart_total_qtde(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])

def cart_total_valor(carrinho):
    return sum(
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional')
            else item.get('preco_quantitativo')
            for item
            in carrinho.values()
        ]
    )

    # return sum([item.get('quantidade') * item.get('preco_unitario_promocional') 
    #     for item 
    #     in carrinho.values()])
