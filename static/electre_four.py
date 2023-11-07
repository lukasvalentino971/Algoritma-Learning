import numpy as np
import math

class ElectreFour:
    def __init__ (self, matrix, weight):
        if type(matrix) != np.ndarray:  
            self.matrix = np.array(matrix)
        else:
            self.matrix = matrix
            
        if type(weight) != np.ndarray:  
            self.weight = np.array(weight)
        else:
            self.weight = weight
            
        self.normalized_matrix = self.normalisasi_matriks(self.matrix)
        self.weighted_matrix = self.pembobotan_matriks(self.normalized_matrix, self.weight)
        self.concordance_set = self.get_himpunan_matriks(self.weighted_matrix, 'Concordance')
        self.discordance_set = self.get_himpunan_matriks(self.weighted_matrix, 'Discordance')
        self.concordance_set_table = self.get_tabel_himpunan(self.weighted_matrix, 'Concordance')
        self.discordance_set_table = self.get_tabel_himpunan(self.weighted_matrix, 'Discordance')
        self.concordance_matrix = self.buat_matriks_condis(self.concordance_set_table, 'Concordance', self.weighted_matrix)
        self.discordance_matrix = self.buat_matriks_disdis(self.discordance_set_table, 'Discordance', self.weighted_matrix)
        self.dominance_concordance_matrix = self.hitung_matriks_dominan(self.concordance_matrix)
        self.dominance_discordance_matrix = self.hitung_matriks_dominan(self.discordance_matrix)
        self.aggregate_dominance_matrix = self.buat_matriks_agregasi(self.dominance_concordance_matrix, self.dominance_discordance_matrix)
        self.eliminated_alternative = self.eliminasi_alternatif(self.dominance_concordance_matrix, self.dominance_discordance_matrix)
        self.aggregate_list, self.aggregate_rank = self.perangkingang_matriks_agregasi(self.aggregate_dominance_matrix)
        self.eliminate_rank = self.perangkingang_eliminasi_alternatif(self.eliminated_alternative)
        
    # Normalisasi Matriks Alternatif
    def normalisasi_matriks(self, matriks):
        baris = len(matriks)
        kolom = len(matriks[0])
        list_pembagi = []

        matriks_ternomalisasi = np.zeros((baris, kolom))

        # Memperoleh nilai pembagi yang dikuadratkan
        for k in range(kolom):
            list_pembagi.append([])
            for l in range(baris):
                list_pembagi[k].append(matriks[l][k]**2)

        for i in range(baris):
            for j in range(kolom):
                matriks_ternomalisasi[i][j] = matriks[i][j]/math.sqrt(sum(list_pembagi[j]))

        return np.array(matriks_ternomalisasi)
    
    # Pembobotan pada matriks yang telah dinormalisasi
    def pembobotan_matriks(self, matriks, bobot):
        baris = len(matriks)
        kolom = len(matriks[0])

        pembobotan_matriks = np.zeros((baris, kolom))

        for i in range(baris):
            for j in range(kolom):
                pembobotan_matriks[i][j] = matriks[i][j] * bobot[j]

        return np.array(pembobotan_matriks)
    
    # List Himpunan Matriks
    def get_himpunan_matriks(self, matriks, tipe):
        baris = len(matriks)

        himpunan_matriks = []

        for i in range(baris):
            for j in range(baris):
                if i == j:
                    continue

                if tipe.lower() == 'concordance':
                    c = f'C{i+1}{j+1}'
                elif tipe.lower() == 'discordance':
                    c = f'D{i+1}{j+1}'
                else:
                    # print('Tipe Tidak Dikenali!!!')
                    return

                himpunan = self.get_himpunan(matriks, tipe, i, j)
                himpunan_c = {c: himpunan}

                himpunan_matriks.append(himpunan_c);

        return himpunan_matriks

    def get_himpunan(matriks, tipe, baris_a, baris_b):
        kolom = len(matriks[0])

        himpunan = []

        for j in range(kolom):

            if tipe.lower() == 'concordance':
                if matriks[baris_a][j] >= matriks[baris_b][j]:
                    himpunan.append(j+1)
            elif tipe.lower() == 'discordance':
                if matriks[baris_a][j] < matriks[baris_b][j]:
                    himpunan.append(j+1)
            else:
                # print('Tipe Tidak Dikenali!!!')
                return

        return himpunan
    
    # Tabel Himpunan
    def get_tabel_himpunan(self, matriks, tipe):
        baris = len(matriks)

        tabel_himpunan = [[0 for j in range(baris)] for i in range(baris)]

        for i in range(baris):
            for j in range(baris):
                if i != j:
                    himpunan = get_himpunan(matriks, tipe, i, j);
                    tabel_himpunan[i][j] = himpunan

        return np.array(tabel_himpunan, dtype=object)
    
    # Matriks Concordance dan Discordance
    def buat_matriks_condis(self, tabel_himpunan, tipe, matriks):
        baris = len(tabel_himpunan)
        kolom = len(tabel_himpunan[0])

        matriks_concordance = np.zeros((baris, kolom))

        for i in range(baris):
            for j in range(kolom):
                if i != j:
                    if tipe.lower() == 'concordance':
                        matriks_concordance[i][j] = hitung_bobot_concordance(tabel_himpunan[i][j])
                    elif tipe.lower() == 'discordance':
                        pembilang = max_himpunan(matriks, i, j, tabel_himpunan[i][j])
                        penyebut = max_himpunan(matriks, i, j)
                        matriks_concordance[i][j] = pembilang/penyebut
                    else:
                        # print('Tipe Tidak Dikenali!!!')
                        return

        return np.array(matriks_concordance)

    # Matriks Connordance
    def hitung_bobot_concordance(self, list_himpunan):
        total_bobot = 0
        for i in list_himpunan:
            total_bobot += bobot[i-1]

        return total_bobot
    
    # Matriks Discordance
    def max_himpunan(self, matriks, baris_a, baris_b, list_himpunan = 0):
        kolom = len(matriks[0])

        list_selisih = []

        for j in range(kolom):
            if list_himpunan != 0:
                if not list_himpunan:
                    return 0
                elif j + 1 in list_himpunan:
                    list_selisih.append(abs(matriks[baris_a][j] - matriks[baris_b][j]))
            else:
                list_selisih.append(abs(matriks[baris_a][j] - matriks[baris_b][j]))

        return max(list_selisih)
    
    # Menghitung Matrik Dominan Concordance dan Discordance
    def hitung_matriks_dominan(self, matriks):
        baris = len(matriks)
        kolom = len(matriks[0])
        c = np.sum(matriks) / (baris * (baris-1))

        matriks_domain = np.zeros((baris, kolom))

        for i in range(baris):
            for j in range(kolom):
                if i != j:
                    if matriks[i][j] >= c:
                        matriks_domain[i][j] = 1

        return np.array(matriks_domain)
    
    # Matriks Agregasi
    def buat_matriks_agregasi(self, matriks_c, matriks_d):
        baris = len(matriks_c)
        kolom = len(matriks_c[0])

        matriks_agregasi = np.zeros((baris, kolom))

        for i in range(baris):
            for j in range(kolom):
                if i != j:
                    matriks_agregasi[i][j] = int(matriks_c[i][j] * matriks_d[i][j])

        return np.array(matriks_agregasi)
    
    # Eliminase alternatif yang less favourable
    def eliminasi_alternatif(self, matriks_c, matriks_d):
        baris = len(matriks_c)
        kolom = len(matriks_c[0])

        list_e = {}
        for i in range(baris):
            alternatif = f'A{i + 1}'
            selisih = []
            for j in range(kolom):
                selisih.append(matriks_c[i][j] - matriks_d[i][j])

            total_selisih = sum(selisih)
            list_e[alternatif] = total_selisih

        return list_e
    
    # Perangkingan Matriks Agregasi
    def perangkingang_matriks_agregasi(self, matriks_agregasi):
        baris = len(matriks_agregasi)

        list_total = []

        for i in range(baris):
            total = sum(matriks_agregasi[i])
            list_total.append(total)
        
        rank = sorted(list_total, reverse=True)

        list_rank = []

        for i in list_total:
            index = rank.index(i)
            list_rank.append(index + 1)

        return list_total, list_rank
    
    # Perangkingan Eliminasi Alternatif
    def perangkingang_eliminasi_alternatif(self, list_e_alternatif):
        rank = sorted(list_e_alternatif.values(), reverse=True)

        list_rank = []

        for i in list_e_alternatif.values():
            index = rank.index(i)
            list_rank.append(index + 1)

        return list_rank