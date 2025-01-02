def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')

def cart_total_qtde(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])

def cart_total_valor(carrinho):
    # total = 0
    # for produto in carrinho.values():
    #     total += (produto['preco_unitario_promocional'] * produto['quantidade'])

    # return f'{total:.2f}'

    # print(f'Carrinho: {carrinho.values()}')
    # print(
    #     sum([item.get('preco_unitario_promocional') 
    #      if item.get('preco_unitario_promocional') 
    #      else item.get('preco_unitario') 
    #      for item 
    #      in carrinho.values()])
    # )

    return sum([item.get('preco_unitario_promocional') 
         if item.get('preco_unitario_promocional') 
         else item.get('preco_unitario') 
         for item 
         in carrinho.values()])

    # return f'R$ {sum([item.get('preco_unitario_promocional') 
    #      if item.get('preco_unitario_promocional') 
    #      else item.get('preco_unitario') 
    #      for item 
    #      in carrinho.values()])}'
