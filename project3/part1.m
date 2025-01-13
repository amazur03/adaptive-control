% ---------- Parametry transmitancji ----------
% Licznik i mianownik transmitancji
numerator = [1, -2];          % Licznik: s - 2
denominator = [1, 13, 36];    % Mianownik: s^2 + 13s + 36

% Utworzenie obiektu transmitancji w MATLAB
sys_tf = tf(numerator, denominator);

% Przekształcenie transmitancji do przestrzeni stanów
[A, B, C, D] = tf2ss(numerator, denominator);

% ---------- Rozwiązywanie ODE za pomocą ode45 ----------
% Funkcja do rozwiązania układu równań różniczkowych (wejście skokowe)
u = 1;  % Wejście skokowe (jednostkowe)
odefun = @(t, x) A * x + B * u;  % Równanie stanu

% Początkowe warunki (zakładamy, że system zaczyna od stanu zerowego)
x0 = [0; 0];  % Stan początkowy (x1 = 0, x2 = 0)

% Zakres czasu (od t = 0 do t = 10)
tspan = [0 10];

% Rozwiązywanie równań różniczkowych za pomocą ode45
[t, x] = ode45(odefun, tspan, x0);

% Obliczanie odpowiedzi wyjściowej (y = Cx)
y = Cc * x';

% Rysowanie wykresu odpowiedzi skokowej
figure;
plot(t, y);
xlabel('Czas (s)');
ylabel('Odpowiedź skokowa y(t)');
title('Odpowiedź skokowa układu');
grid on;

% ---------- Regulacja Proporcjonalna ----------
% Wartość zadana
y_z = 1;      % Wartość zadana wyjścia
kp = 1;       % Wzmocnienie regulatora proporcjonalnego

% Równanie różniczkowe z regulatorem proporcjonalnym
odefun_regulator = @(t, x) A * x + B * (kp * (y_z - Cc * x));

% Rozwiązywanie równań różniczkowych
[t, x2] = ode45(odefun_regulator, tspan, x0);

% Obliczanie odpowiedzi wyjściowej (y = Cx)
y2 = Cc * x2';

% Rysowanie wykresu odpowiedzi układu regulowanego
figure;
plot(t, y2);
xlabel('Czas (s)');
ylabel('Odpowiedź układu regulowanego y(t)');
title('Odpowiedź układu z regulatorem P');
grid on;

% ---------- Regulacja LQR ----------
% Parametry regulacji
Q = eye(2);   % Penalizacja stanów
R = 0.1;      % Penalizacja sterowania

% Obliczenie macierzy wzmocnienia LQR
K = lqr(A, B, Q, R);

% Wartość zadana wyjścia
y_z = 1;

% Obliczenie wartości odniesienia (x_ref i u_ref)
x_ref = [0; -0.5];  % Wartość odniesienia stanu
u_ref = -18;        % Wartość odniesienia sterowania

% Równanie różniczkowe z regulacją LQR
odefun_lqr = @(t, x) A * x + B * (u_ref - K * (x - x_ref));

% Rozwiązywanie równań różniczkowych
[t, x_lqr] = ode45(odefun_lqr, tspan, x0);

% Obliczanie odpowiedzi wyjściowej (y = Cx)
y_lqr = C * x_lqr';

% Rysowanie wykresu odpowiedzi
figure;
plot(t, y_lqr);
xlabel('Czas (s)');
ylabel('Odpowiedź wyjściowa y(t)');
title('Odpowiedź układu z regulatorem LQR');
grid on;

% ---------- Obserwator stanu Luenbergera ----------

% Definicja biegunów obserwatora
poles = [-1, -1.5]; 

% Obliczenie macierzy L za pomocą funkcji acker
L = acker(A', C', poles)';

% Obliczenie macierzy A_observer
A_observer = A - L * C;

% Inicjalizacja początkowego wektora stanu obserwatora
x_hat_0 = [0.5; 0.5];

% Czas symulacji
sim_time = 10;

% Czas skoku
czas_skok = 0;

% Symulacja modelu z pliku .slx
[out] = sim("part2s.slx", sim_time);

% ---------- Wizualizacja wyników ----------

% 1. Wyjście obiektu
figure;
plot(out.tout, out.simout_y);
xlabel('Czas (s)');
ylabel('Odpowiedź obiektu y(t)');
title('Zmiana wyjścia obiektu w czasie');
grid on;

% 2. Wyjście modelu (obserwatora)
figure;
plot(out.tout, out.simout_yhat);
xlabel('Czas (s)');
ylabel('Odpowiedź obserwatora y_{hat}(t)');
title('Zmiana wyjścia modelu w czasie');
grid on;

% 3. Różnica między wyjściami obiektu a obserwatora
figure;
y_diff = out.simout_yhat - out.simout_y;
plot(out.tout, y_diff);
xlabel('Czas (s)');
ylabel('Różnica wyjść');
title('Różnica wyjść obiektu i obserwatora w czasie');
grid on;

% 4. Stan obiektu (X)
figure;
plot(out.tout, out.simout_x);
xlabel('Czas (s)');
ylabel('Stan obiektu x(t)');
title('Zmiana stanu obiektu w czasie');
grid on;

% 5. Stan modelu (obserwatora)
figure;
plot(out.tout, out.simout_xhat);
xlabel('Czas (s)');
ylabel('Stan obserwatora x_{hat}(t)');
title('Zmiana stanu modelu w czasie');
grid on;

% 6. Błąd stanu (różnica między stanem obiektu a obserwatora)
figure;
plot(out.tout, epsilon(:, 1), 'r');  % Błąd dla pierwszego stanu
hold on;
plot(out.tout, epsilon(:, 2), 'g');  % Błąd dla drugiego stanu
xlabel('Czas (s)');
ylabel('\epsilon');
title('Błąd stanu: różnica x obiektu i modelu');
grid on;
legend({'Błąd stanu 1', 'Błąd stanu 2'}, 'Location', 'Best');