/**
 * calcular_media.c
 * Função C para calcular média de notas (NP1, NP2, PIM)
 * 
 * Compilar:
 *   Windows: gcc -shared -o calcular_media.dll calcular_media.c
 *   Linux:   gcc -shared -fPIC -o calcular_media.so calcular_media.c
 *   Mac:     gcc -shared -fPIC -o calcular_media.dylib calcular_media.c
 */

/**
 * Calcula a média de três notas
 * @param np1 Nota da primeira avaliação (0-10)
 * @param np2 Nota da segunda avaliação (0-10)
 * @param pim Nota do PIM (0-10)
 * @return Média calculada (np1 + np2 + pim) / 3.0
 */
double calcular_media(double np1, double np2, double pim) {
    return (np1 + np2 + pim) / 3.0;
}

