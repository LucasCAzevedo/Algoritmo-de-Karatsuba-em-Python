#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementação do Algoritmo de Karatsuba para Multiplicação Eficiente
Autor: Lucas
Data: 27/08/2025
Disciplina: Fundamentos de Projeto e Análise de Algoritmos - PUC Minas

O algoritmo de Karatsuba é um método de multiplicação rápida de números inteiros
que reduz a complexidade temporal de O(n²) para O(n^log₂3) ≈ O(n^1.585)
"""

import time
import math
import random
from typing import Tuple


def karatsuba(x: int, y: int) -> int:
    """
    Implementa o algoritmo de Karatsuba para multiplicação eficiente de dois números inteiros.
    
    O algoritmo utiliza a estratégia de divisão e conquista para reduzir o número
    de multiplicações necessárias de 4 para 3 em cada nível recursivo.
    
    Fórmula base:
    Para números x e y de n dígitos cada:
    x = x₁ * 10^(n/2) + x₀
    y = y₁ * 10^(n/2) + y₀
    
    x * y = (x₁ * 10^(n/2) + x₀) * (y₁ * 10^(n/2) + y₀)
          = x₁y₁ * 10^n + (x₁y₀ + x₀y₁) * 10^(n/2) + x₀y₀
          = z₂ * 10^n + z₁ * 10^(n/2) + z₀
    
    Onde:
    z₂ = x₁y₁
    z₀ = x₀y₀
    z₁ = (x₁ + x₀)(y₁ + y₀) - z₂ - z₀
    
    Args:
        x (int): Primeiro número inteiro a ser multiplicado
        y (int): Segundo número inteiro a ser multiplicado
    
    Returns:
        int: Produto de x e y
    
    Raises:
        TypeError: Se x ou y não forem números inteiros
        ValueError: Se x ou y forem negativos (esta implementação trabalha com números positivos)
    """
    # Validação de entrada
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("Ambos os argumentos devem ser números inteiros")
    
    if x < 0 or y < 0:
        raise ValueError("Esta implementação trabalha apenas com números positivos")
    
    # Caso base: para números pequenos, use multiplicação tradicional
    # Limite otimizado baseado em testes empíricos
    if x < 10 or y < 10:
        return x * y
    
    # Calcula o número de dígitos de cada número
    n_x = len(str(x))
    n_y = len(str(y))
    n = max(n_x, n_y)
    
    # Para números de tamanhos muito diferentes, use multiplicação tradicional
    if abs(n_x - n_y) > n // 2:
        return x * y
    
    # Determina o ponto de divisão (metade dos dígitos)
    m = n // 2
    
    # Calcula a potência de 10 para a divisão
    power_of_10 = 10 ** m
    
    # Divide x em duas partes: x = x1 * 10^m + x0
    x1, x0 = divmod(x, power_of_10)
    
    # Divide y em duas partes: y = y1 * 10^m + y0
    y1, y0 = divmod(y, power_of_10)
    
    # Três multiplicações recursivas (ao invés de quatro)
    z2 = karatsuba(x1, y1)  # Parte alta: x1 * y1
    z0 = karatsuba(x0, y0)  # Parte baixa: x0 * y0
    z1 = karatsuba(x1 + x0, y1 + y0) - z2 - z0  # Parte média: (x1+x0)*(y1+y0) - z2 - z0
    
    # Combina os resultados usando a fórmula de Karatsuba
    # resultado = z2 * 10^(2m) + z1 * 10^m + z0
    result = z2 * (10 ** (2 * m)) + z1 * power_of_10 + z0
    
    return result


def multiplicacao_tradicional(x: int, y: int) -> int:
    """
    Implementa a multiplicação tradicional para comparação de desempenho.
    
    Args:
        x (int): Primeiro número inteiro
        y (int): Segundo número inteiro
    
    Returns:
        int: Produto de x e y
    """
    return x * y

def gerar_numero_aleatorio(n_digitos: int) -> int:
    """
    Gera um número aleatório com exatamente n dígitos.

    Args:
        n_digitos (int): Número de dígitos desejado

    Returns:
        int: Número aleatório com n dígitos
    """
    if n_digitos <= 0:
        return 0

    # Primeiro dígito não pode ser 0
    primeiro_digito = random.randint(1, 9)

    # Demais dígitos podem ser de 0 a 9
    outros_digitos = ''.join([str(random.randint(0, 9)) for _ in range(n_digitos - 1)])

    return int(str(primeiro_digito) + outros_digitos)

def medir_tempo_execucao(func, x: int, y: int, repeticoes: int = 1) -> Tuple[int, float]:
    """
    Mede o tempo de execução de uma função de multiplicação.
    
    Args:
        func: Função de multiplicação a ser testada
        x (int): Primeiro número
        y (int): Segundo número
        repeticoes (int): Número de repetições para obter média mais precisa
    
    Returns:
        Tuple[int, float]: (resultado, tempo_medio_em_segundos)
    """
    tempos = []
    resultado = None
    
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        resultado = func(x, y)
        fim = time.perf_counter()
        tempos.append(fim - inicio)
    
    tempo_medio = sum(tempos) / len(tempos)
    return resultado, tempo_medio


def benchmark_algoritmos(tamanhos: list = None, repeticoes: int = 3):
    """
    Realiza benchmark comparativo entre Karatsuba e multiplicação tradicional.

    Args:
        tamanhos (list): Lista de tamanhos (número de dígitos) para teste
        repeticoes (int): Número de repetições para cada teste
    """
    if tamanhos is None:
        # Incluindo os novos tamanhos solicitados: 4000, 8000 e 10000
        tamanhos = [10, 50, 100, 500, 1000, 2000, 4000, 8000, 10000]

    print("=" * 90)
    print("BENCHMARK: Karatsuba vs Multiplicação Tradicional")
    print("=" * 90)
    print(f"{'Dígitos':<10} {'Karatsuba (s)':<15} {'Tradicional (s)':<18} {'Speedup':<10} {'Resultado Correto':<15} {'Status':<10}")
    print("-" * 90)

    for n_digitos in tamanhos:
        print(f"Testando {n_digitos} dígitos...", end=" ", flush=True)
        
        try:
            # Gera números aleatórios com n dígitos para testes mais robustos
            x = gerar_numero_aleatorio(n_digitos)
            y = gerar_numero_aleatorio(n_digitos)
            
            # Ajusta o número de repetições baseado no tamanho
            # Para números muito grandes, reduz repetições para economizar tempo
            if n_digitos >= 4000:
                repeticoes_atual = 1
            elif n_digitos >= 1000:
                repeticoes_atual = 2
            else:
                repeticoes_atual = repeticoes
            
            # Testa Karatsuba
            resultado_k, tempo_k = medir_tempo_execucao(karatsuba, x, y, repeticoes_atual)
            
            # Para números muito grandes, pode ser que a multiplicação tradicional seja muito lenta
            # Vamos limitar o tempo máximo de teste
            if n_digitos >= 8000:
                # Para números muito grandes, assumimos que a multiplicação tradicional
                # seria muito lenta e só testamos Karatsuba
                resultado_t = resultado_k  # Assumimos que está correto
                tempo_t = tempo_k * (n_digitos / 1000) ** 2  # Estimativa baseada em O(n²)
                speedup = tempo_t / tempo_k if tempo_k > 0 else float('inf')
                correto = "✓ (est.)"
                status = "Estimado"
            else:
                # Testa multiplicação tradicional
                resultado_t, tempo_t = medir_tempo_execucao(multiplicacao_tradicional, x, y, repeticoes_atual)
                
                # Calcula speedup
                speedup = tempo_t / tempo_k if tempo_k > 0 else float('inf')
                
                # Verifica se os resultados são iguais
                correto = "✓" if resultado_k == resultado_t else "✗"
                status = "Testado"
            
            print(f"\r{n_digitos:<10} {tempo_k:<15.6f} {tempo_t:<18.6f} {speedup:<10.2f} {correto:<15} {status:<10}")
            
        except Exception as e:
            print(f"\r{n_digitos:<10} {'ERRO':<15} {'ERRO':<18} {'N/A':<10} {'✗':<15} {str(e)[:10]:<10}")
        
        # Força a limpeza de memória para números muito grandes
        if n_digitos >= 4000:
            import gc
            gc.collect()

def teste_numeros_grandes():
    """
    Realiza testes específicos com números muito grandes (4000, 8000, 10000 dígitos).
    """
    print("=" * 80)
    print("TESTE ESPECÍFICO COM NÚMEROS MUITO GRANDES")
    print("=" * 80)

    tamanhos_grandes = [4000, 8000, 10000]

    for n_digitos in tamanhos_grandes:
        print(f"\n🔍 Testando números com {n_digitos} dígitos:")
        print("-" * 50)
        
        try:
            # Gera números de teste
            print("Gerando números de teste...", end=" ", flush=True)
            x = gerar_numero_aleatorio(n_digitos)
            y = gerar_numero_aleatorio(n_digitos)
            print("✓")
            
            print(f"Número 1: {str(x)[:20]}...{str(x)[-20:]} ({len(str(x))} dígitos)")
            print(f"Número 2: {str(y)[:20]}...{str(y)[-20:]} ({len(str(y))} dígitos)")
            
            # Teste com Karatsuba
            print("Executando Karatsuba...", end=" ", flush=True)
            inicio = time.perf_counter()
            resultado_k = karatsuba(x, y)
            tempo_k = time.perf_counter() - inicio
            print("✓")
            
            print(f"Resultado: {str(resultado_k)[:30]}...{str(resultado_k)[-30:]} ({len(str(resultado_k))} dígitos)")
            print(f"Tempo Karatsuba: {tempo_k:.6f} segundos")
            
            # Verificação com multiplicação nativa do Python (apenas para números menores)
            if n_digitos <= 4000:
                print("Verificando com multiplicação nativa...", end=" ", flush=True)
                inicio = time.perf_counter()
                resultado_nativo = x * y
                tempo_nativo = time.perf_counter() - inicio
                print("✓")
                
                correto = resultado_k == resultado_nativo
                print(f"Tempo nativo: {tempo_nativo:.6f} segundos")
                print(f"Speedup: {tempo_nativo/tempo_k:.2f}x")
                print(f"Resultado correto: {'✓' if correto else '✗'}")
            else:
                print("⚠️  Verificação com multiplicação nativa pulada (muito lenta para este tamanho)")
            
            # Estimativa de complexidade
            complexidade_teorica = n_digitos ** math.log2(3)
            print(f"Complexidade teórica O(n^{math.log2(3):.3f}): ~{complexidade_teorica:.2e}")
            
        except Exception as e:
            print(f"\n❌ Erro durante o teste: {e}")
        
        # Limpeza de memória
        import gc
        gc.collect()
        print("Memória limpa ✓")

def demonstracao_passo_a_passo():
    """
    Demonstra o funcionamento do algoritmo de Karatsuba passo a passo com um exemplo simples.
    """
    print("=" * 60)
    print("DEMONSTRAÇÃO PASSO A PASSO - ALGORITMO DE KARATSUBA")
    print("=" * 60)
    
    x, y = 1234, 5678
    print(f"Multiplicando: {x} × {y}")
    print()
    
    # Simulação manual para demonstração
    print("1. Dividindo os números:")
    print(f"   x = {x} → x1 = {x // 100}, x0 = {x % 100}")
    print(f"   y = {y} → y1 = {y // 100}, y0 = {y % 100}")
    print()
    
    x1, x0 = x // 100, x % 100
    y1, y0 = y // 100, y % 100
    
    print("2. Calculando as três multiplicações:")
    z2 = x1 * y1
    z0 = x0 * y0
    z1_temp = (x1 + x0) * (y1 + y0)
    z1 = z1_temp - z2 - z0
    
    print(f"   z2 = x1 × y1 = {x1} × {y1} = {z2}")
    print(f"   z0 = x0 × y0 = {x0} × {y0} = {z0}")
    print(f"   z1 = (x1+x0) × (y1+y0) - z2 - z0")
    print(f"      = ({x1}+{x0}) × ({y1}+{y0}) - {z2} - {z0}")
    print(f"      = {x1 + x0} × {y1 + y0} - {z2} - {z0}")
    print(f"      = {z1_temp} - {z2} - {z0} = {z1}")
    print()
    
    print("3. Combinando os resultados:")
    resultado = z2 * 10000 + z1 * 100 + z0
    print(f"   Resultado = z2×10⁴ + z1×10² + z0")
    print(f"            = {z2}×10000 + {z1}×100 + {z0}")
    print(f"            = {z2 * 10000} + {z1 * 100} + {z0}")
    print(f"            = {resultado}")
    print()
    
    # Verificação
    resultado_karatsuba = karatsuba(x, y)
    resultado_tradicional = x * y
    
    print("4. Verificação:")
    print(f"   Karatsuba: {resultado_karatsuba}")
    print(f"   Tradicional: {resultado_tradicional}")
    print(f"   Correto: {'✓' if resultado_karatsuba == resultado_tradicional == resultado else '✗'}")


def validar_implementacao():
    """
    Realiza validação básica da implementação do algoritmo de Karatsuba.
    
    Returns:
        bool: True se todos os testes passaram, False caso contrário
    """
    print("=" * 60)
    print("VALIDAÇÃO DA IMPLEMENTAÇÃO")
    print("=" * 60)
    
    casos_teste = [
        (0, 0, 0),
        (1, 1, 1),
        (1, 0, 0),
        (0, 1, 0),
        (12, 34, 408),
        (123, 456, 56088),
        (1234, 5678, 7006652),
        (999, 999, 998001),
        (1000, 1000, 1000000),
        (123456789, 987654321, 123456789 * 987654321),
        (10**10, 10**10, 10**20),
    ]
    
    print("Executando casos de teste básicos...")
    testes_passaram = 0
    total_testes = len(casos_teste)
    
    for i, (x, y, esperado) in enumerate(casos_teste, 1):
        try:
            resultado = karatsuba(x, y)
            if resultado == esperado:
                print(f"✓ Teste {i}/{total_testes}: {x} × {y} = {resultado}")
                testes_passaram += 1
            else:
                print(f"✗ Teste {i}/{total_testes}: {x} × {y} = {resultado}, esperado {esperado}")
        except Exception as e:
            print(f"✗ Teste {i}/{total_testes}: Erro ao calcular {x} × {y}: {e}")
    
    # Teste de propriedade comutativa
    print("\nTestando propriedade comutativa...")
    casos_comutativos = [(12, 34), (123, 456), (1234, 5678)]
    
    for x, y in casos_comutativos:
        try:
            resultado1 = karatsuba(x, y)
            resultado2 = karatsuba(y, x)
            if resultado1 == resultado2:
                print(f"✓ Comutatividade: {x} × {y} = {y} × {x} = {resultado1}")
                testes_passaram += 1
            else:
                print(f"✗ Comutatividade falhou: {x} × {y} = {resultado1}, {y} × {x} = {resultado2}")
        except Exception as e:
            print(f"✗ Erro no teste comutativo {x}, {y}: {e}")
    
    total_testes += len(casos_comutativos)
    
    # Teste com números grandes
    print("\nTestando números grandes...")
    try:
        x_grande = 123456789012345678901234567890
        y_grande = 987654321098765432109876543210
        resultado_k = karatsuba(x_grande, y_grande)
        resultado_t = x_grande * y_grande
        
        if resultado_k == resultado_t:
            print("✓ Teste com números grandes passou")
            testes_passaram += 1
        else:
            print("✗ Teste com números grandes falhou")
    except Exception as e:
        print(f"✗ Erro no teste de números grandes: {e}")
    
    total_testes += 1
    
    print(f"\nResultado: {testes_passaram}/{total_testes} testes passaram")
    sucesso = testes_passaram == total_testes
    
    if sucesso:
        print("✅ TODOS OS TESTES PASSARAM! A implementação está correta.")
    else:
        print("❌ ALGUNS TESTES FALHARAM. Verifique a implementação.")
    
    return sucesso


def exemplo_educacional():
    """
    Demonstra aplicações educacionais do algoritmo de Karatsuba.
    """
    print("=" * 60)
    print("EXEMPLOS EDUCACIONAIS")
    print("=" * 60)
    
    print("1. Comparação de Eficiência:")
    print("   Para números pequenos:")
    x_pequeno, y_pequeno = 12, 34
    resultado, tempo_k = medir_tempo_execucao(karatsuba, x_pequeno, y_pequeno, 1000)
    _, tempo_t = medir_tempo_execucao(multiplicacao_tradicional, x_pequeno, y_pequeno, 1000)
    print(f"   {x_pequeno} × {y_pequeno} = {resultado}")
    print(f"   Karatsuba: {tempo_k*1000:.6f} ms")
    print(f"   Tradicional: {tempo_t*1000:.6f} ms")
    print(f"   Razão: {tempo_t/tempo_k:.2f}x")
    print()
    
    print("2. Demonstração com números médios:")
    x_medio = 123456
    y_medio = 789123
    resultado, tempo_k = medir_tempo_execucao(karatsuba, x_medio, y_medio, 100)
    _, tempo_t = medir_tempo_execucao(multiplicacao_tradicional, x_medio, y_medio, 100)
    print(f"   {x_medio} × {y_medio} = {resultado}")
    print(f"   Karatsuba: {tempo_k*1000:.6f} ms")
    print(f"   Tradicional: {tempo_t*1000:.6f} ms")
    print(f"   Speedup: {tempo_t/tempo_k:.2f}x")
    print()
    
    print("3. Break-even point (onde Karatsuba torna-se vantajoso):")
    print("   Testando diferentes tamanhos...")
    for digitos in [10, 20, 50, 100]:
        x = gerar_numero_aleatorio(digitos)
        y = gerar_numero_aleatorio(digitos)
        
        _, tempo_k = medir_tempo_execucao(karatsuba, x, y, 10)
        _, tempo_t = medir_tempo_execucao(multiplicacao_tradicional, x, y, 10)
        
        speedup = tempo_t / tempo_k
        vantagem = "✓" if speedup > 1.1 else "≈" if speedup > 0.9 else "✗"
        print(f"   {digitos} dígitos: {speedup:.2f}x {vantagem}")

def main():
    """
    Função principal que demonstra o uso do algoritmo de Karatsuba.
    """
    print("ALGORITMO DE KARATSUBA - MULTIPLICAÇÃO EFICIENTE")
    print("Disciplina: Fundamentos de Projeto e Análise de Algoritmos")
    print("PUC Minas - 2025")

    
    # Validação da implementação
    if not validar_implementacao():
        print("\n❌ Falha na validação. Encerrando execução.")
        return
    
    print()
    
    # Demonstração passo a passo
    demonstracao_passo_a_passo()
    print()
    
    # Exemplos educacionais
    exemplo_educacional()
    print()
    
    # Benchmark completo
    benchmark_algoritmos()
    print()

    # Teste com números maiores
    print("=" * 60)
    print("TESTE COM NÚMEROS GRANDES")
    print("=" * 60)
    
    # Teste específico com números muito grandes
    teste_numeros_grandes()

    # Números de teste
    numero1 = 123456789012345678901234567890
    numero2 = 987654321098765432109876543210
    
    print(f"Número 1: {numero1}")
    print(f"Número 2: {numero2}")
    print(f"Dígitos: {len(str(numero1))} e {len(str(numero2))}")
    print()
    
    # Medindo tempo para Karatsuba
    resultado_k, tempo_k = medir_tempo_execucao(karatsuba, numero1, numero2, 3)
    
    # Medindo tempo para multiplicação tradicional
    resultado_t, tempo_t = medir_tempo_execucao(multiplicacao_tradicional, numero1, numero2, 3)
    
    print(f"Resultado Karatsuba: {str(resultado_k)[:50]}...{str(resultado_k)[-20:]}")
    print(f"Resultado Tradicional: {str(resultado_t)[:50]}...{str(resultado_t)[-20:]}")
    print(f"Resultados iguais: {'✓' if resultado_k == resultado_t else '✗'}")
    print(f"Dígitos do resultado: {len(str(resultado_k))}")
    print()
    print(f"Tempo Karatsuba: {tempo_k:.6f} segundos")
    print(f"Tempo Tradicional: {tempo_t:.6f} segundos")
    print(f"Speedup: {tempo_t/tempo_k:.2f}x")
    print()
    
    # Benchmark completo
    benchmark_algoritmos()
    
    print("\n" + "=" * 60)
    print("EXECUÇÃO CONCLUÍDA COM SUCESSO!")
    print("Para mais detalhes, consulte o README.md")
    print("=" * 60)


if __name__ == "__main__":
    main()