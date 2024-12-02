import numpy as np
import matplotlib.pyplot as plt

# ======== ETAP 1: Generowanie danych wejściowych i wyjściowych ======== #
# Definicja rzeczywistego parametru modelu (theta*)
theta_g = [1, 1, 1]

# Inicjalizacja tablic na dane wejściowe i wyjściowe
u = np.zeros(100)  # Tablica wejść
y = np.zeros(100)  # Tablica wyjść

# Generowanie danych wejściowych i wyjściowych
for k in range(2, 100):
    # Zakłócenia o rozkładzie normalnym (średnia 0, wariancja 0.05)
    z = np.random.randn() * np.sqrt(0.05)
    
    # Generowanie wejść jako liczby losowe z przedziału [-10, 10]
    u[k] = np.random.rand() * 20 - 10
    
    # Obliczanie wyjść na podstawie rzeczywistego modelu
    y[k] = theta_g[0] * u[k] + theta_g[1] * u[k-1] + theta_g[2] * u[k-2] + z

# ======== ETAP 2: Estymacja parametrów rzeczywistego modelu ======== #

# Inicjalizacja estymatora (theta z daszkiem)
theta_e = np.zeros((100, 3, 1))  # Tablica 100 macierzy 3x1

# Inicjalizacja macierzy wagowych (P) o wymiarach 3x3
p = np.zeros((100, 3, 3))
# Początkowe wartości macierzy wagowej
p[0] = np.eye(3) * 100
p[1] = np.eye(3) * 100

# Proces estymacji parametrów
for k in range(2, 100):
    # Macierz fi (phi) zawierająca ostatnie wartości wejść
    phi = np.array([[u[k]],
                    [u[k-1]],
                    [u[k-2]]])
    
    # Aktualizacja macierzy wagowej P
    p[k] = p[k-1] - (p[k-1] @ phi @ phi.T @ p[k-1]) / (1 + phi.T @ p[k-1] @ phi)
    
    # Aktualizacja estymatora theta_e
    theta_e[k] = theta_e[k-1] + (p[k] @ phi * (y[k] - phi.T @ theta_e[k-1]))

# Wizualizacja wyników estymacji
theta_e_values = theta_e.reshape(100, 3)  # Konwersja estymatora na tablicę 2D

plt.figure(figsize=(10, 6))
plt.plot(range(100), theta_e_values[:, 0], label=r'$\Theta_{e1}$', color = "r")
plt.plot(range(100), theta_e_values[:, 1], label=r'$\Theta_{e2}$', color='g')
plt.plot(range(100), theta_e_values[:, 2], label=r'$\Theta_{e3}$', color='b')
plt.axhline(1, color='magenta', linestyle='--', label=r'Prawdziwe $\Theta_g$')
plt.title(r'Zmiana estymatora $\Theta_e$ w czasie', fontsize=14)
plt.xlabel('Iteracja', fontsize=12)
plt.ylabel(r'Wartość $\Theta$', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()



# ======== SPRAWDZAMY MSE DLA KAZDEJ LAMBDY ======== #
# Funkcja obliczająca MSE dla danego lambda
def calculate_mse(lambdaa):
    # Inicjalizacja estymatora i macierzy wagowych
    theta_e = np.zeros((100, 3, 1))
    p = np.zeros((100, 3, 3))
    p[0] = np.eye(3) * 100
    p[1] = np.eye(3) * 100
    
    # Ponowne generowanie danych
    u = np.zeros(100)  # Tablica wejść
    y = np.zeros(100)  # Tablica wyjść
    theta_g = [1, 1, 1]

    for k in range(2, 100):
        theta_g[1] = 0.1 * np.sin(0.1 * k) + 1
        z = 0.1 * np.sin(0.1 * k) + 1 + np.random.normal(0, 0.05)
        u[k] = np.random.rand() * 20 - 10
        y[k] = theta_g[0] * u[k] + theta_g[1] * u[k-1] + theta_g[2] * u[k-2] + z

    # Proces estymacji z zapominaniem
    for k in range(2, 100):
        phi = np.array([[u[k]], [u[k-1]], [u[k-2]]])
        p[k] = (1 / lambdaa) * (p[k-1] - (p[k-1] @ phi @ phi.T @ p[k-1]) / (lambdaa + phi.T @ p[k-1] @ phi))
        theta_e[k] = theta_e[k-1] + (p[k] @ phi * (y[k] - phi.T @ theta_e[k-1]))

    # Obliczenie MSE
    theta_e_values = theta_e.reshape(100, 3)  # Konwersja na tablicę 2D
    theta_g_values = [(1, 0.1 * np.sin(0.1 * k) + 1, 1) for k in range(100)]  # Prawdziwe wartości theta_g
    theta_g_values = np.array(theta_g_values)

    mse = np.mean((theta_e_values - theta_g_values) ** 2)
    return mse

# Zakres lambdy
lambda_values = np.linspace(0.01, 0.99, 100)

# Tablica na wartości MSE
mse_values = []

# Iteracja po różnych wartościach lambdy
for lambdaa in lambda_values:
    mse = calculate_mse(lambdaa)
    mse_values.append(mse)

# Wizualizacja MSE dla różnych wartości lambdy
plt.figure(figsize=(10, 6))
plt.plot(lambda_values, mse_values, label="MSE")
plt.title("MSE dla różnych wartości lambdy", fontsize=14)
plt.xlabel("Lambda", fontsize=12)
plt.ylabel("MSE", fontsize=12)
plt.xticks(np.arange(0.01, 0.99, 0.06))
plt.grid(True)
plt.legend(fontsize=12)
plt.show()



# ======== ETAP 3: Estymacja z zapominaniem i dynamicznym modelem ======== #

# Rzeczywiste parametry modelu z dynamiczną zmianą theta_g[1]
theta_g = [1, 1, 1]

# Ponowne generowanie danych
u = np.zeros(100)  # Tablica wejść
y = np.zeros(100)  # Tablica wyjść

for k in range(2, 100):
    # Zmienny parametr theta_g[1] jako sinusoidalne zmiany
    theta_g[1] = 0.1 * np.sin(0.1 * k) + 1
    
    # Zakłócenia: sinusoidalne + losowe
    z = 0.1 * np.sin(0.1 * k) + 1 + np.random.normal(0, 0.05)
    
    # Generowanie wejść jako liczby losowe z przedziału [-10, 10]
    u[k] = np.random.rand() * 20 - 10
    
    # Obliczanie wyjść na podstawie dynamicznego modelu
    y[k] = theta_g[0] * u[k] + theta_g[1] * u[k-1] + theta_g[2] * u[k-2] + z

# Inicjalizacja estymatora i macierzy wagowych
theta_e = np.zeros((100, 3, 1))
p = np.zeros((100, 3, 3))
p[0] = np.eye(3) * 100
p[1] = np.eye(3) * 100

# Czynnik zapominania
lambdaa = 0.9

# Proces estymacji z zapominaniem
for k in range(2, 100):
    # Macierz phi zawierająca ostatnie wartości wejść
    phi = np.array([[u[k]],
                    [u[k-1]],
                    [u[k-2]]])
    
    # Aktualizacja macierzy wagowej P z uwzględnieniem zapominania
    p[k] = (1 / lambdaa) * (p[k-1] - (p[k-1] @ phi @ phi.T @ p[k-1]) / (lambdaa + phi.T @ p[k-1] @ phi))
    
    # Aktualizacja estymatora theta_e
    theta_e[k] = theta_e[k-1] + (p[k] @ phi * (y[k] - phi.T @ theta_e[k-1]))

# Przygotowanie danych do wizualizacji
theta_e_values = theta_e.reshape(100, 3)  # Konwersja na tablicę 2D
theta_g_values = [(1, 0.1 * np.sin(0.1 * k) + 1, 1) for k in range(100)]  # Prawdziwe wartości theta_g
theta_g_values = np.array(theta_g_values)

# Wizualizacja estymatorów i rzeczywistych parametrów
plt.figure(figsize=(12, 8))
plt.plot(range(100), theta_e_values[:, 0], label=r'Estymator $\Theta_{e1}$', color ='r')
plt.plot(range(100), theta_e_values[:, 1], label=r'Estymator $\Theta_{e2}$', color= 'g')
plt.plot(range(100), theta_e_values[:, 2], label=r'Estymator $\Theta_{e3}$', color= 'b')
plt.plot(range(100), theta_g_values[:, 1], label=r'Prawdziwe $\Theta_{g2}$', color = 'magenta')
plt.axhline(1, color='magenta', linestyle='-.', label=r'Prawdziwe $\Theta_{g1}$ i $\Theta_{g3}$')
plt.title(r'Zmiana estymatora $\Theta_e$ oraz rzeczywistej wartości $\Theta_g$', fontsize=14)
plt.xlabel('Iteracja', fontsize=12)
plt.ylabel(r'$\Theta$', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True)
plt.show()


# ======== ETAP 4: Sterowanie adaptacyjne ======== #
# losujemy nasze żądanie (żądanie to to co ma być na wyjściu)
d = np.random.uniform(-10,10)

# inicjalizujemy tablice dla wejść
u = np.zeros(100)
y = np.zeros(100) #wyjscia

# przepisujemy "aktualne" ("najświeższe") theta estymowane
# i macierz wagową do indeksu 2)
# ponieważ nową pętle będziemy indeksować od 2
theta_e[2] = theta_e[99]
p[2] = p[99]

for k in range(2, 100):
    # sygnał wejściowy
    u[k] = (d - theta_e[k][1, 0] * u[k-1] - theta_e[k][2, 0] * u[k-2]) / theta_e[k][0, 0]

    # drugi parametr obiektu zmienny w czasie
    # sinus w zakresie od 0.9 do 1.1 z powolnymi zmianami
    theta_g[1] = (0.1 * np.sin(0.1*k)) + 1

    # zakłócenia - liczby losowe z przedziału -0.1 do 0.1
    z = np.random.rand() * 0.1 * 2 - 0.1

    # wyjscie obiektu
    y[k] = theta_g[0] * u[k] + theta_g[1] * u[k - 1] + theta_g[2] * u[k - 2] + z


    # phi (czyt. fi) jako macierz 3x1 - macierz wejść
    phi = np.array([[u[k]],
                    [u[k - 1]],
                    [u[k - 2]]])

    # liczymy macierz wagową 'p' dla chwili 'k'
    p[k] = (1 / lambdaa) * (p[k-1] - ((p[k-1] @ phi @ phi.T @ p[k-1]) / (lambdaa + phi.T @ p[k-1] @ phi)))

    # liczymy estymator w chwili 'k'
    theta_e[k] = theta_e[k-1] + (p[k] @ phi * (y[k] - phi.T @ theta_e[k-1]))


plt.figure(figsize=(12, 8))

# Wykres żądania (d)
plt.plot(range(100), [d] * 100, label='Żądanie (d)', color='magenta')

# Wykres wejścia sterującego (u[k])
plt.plot(range(100), u, label='Wejście sterujące (u[k])', color='r')

# Wykres wyjścia systemu (y[k])
plt.plot(range(100), y, label='Wyjście systemu (y[k])', color='g')

# Tytuł i osie
plt.title('Porównanie żądania, wejścia sterującego i wyjścia systemu', fontsize=14)
plt.xlabel('Iteracja', fontsize=12)
plt.ylabel('Wartość', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True)
plt.show()