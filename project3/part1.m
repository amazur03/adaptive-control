% ---------- Parametry transmitancji ----------
% Licznik i mianownik transmitancji
numerator = [1, -2];          % Licznik: s - 2
denominator = [1, 13, 36];    % Mianownik: s^2 + 13s + 36

% Utworzenie obiektu transmitancji w MATLAB
sys_tf = tf(numerator, denominator);

% Przekształcenie transmitancji do przestrzeni stanów
[Ac, Bc, Cc, Dc] = tf2ss(numerator, denominator);

% Wyświetlenie macierzy przestrzeni stanów
disp('Macierze przestrzeni stanów:');
disp('A ='); disp(Ac);
disp('B ='); disp(Bc);
disp('C ='); disp(Cc);
disp('D ='); disp(Dc);

% ---------- Rozwiązywanie ODE za pomocą ode45 ----------
% Funkcja do rozwiązania układu równań różniczkowych (wejście skokowe)
u = 1;  % Wejście skokowe (jednostkowe)
odefun = @(t, x) Ac * x + Bc * u;  % Równanie stanu

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
y_z = 1;  % Wartość zadana
kp = 1;  % Wzmocnienie regulatora proporcjonalnego

% Rozwiązywanie ODE z regulacją proporcjonalną
odefun_regulator = @(t, x) Ac * x + Bc * (kp * (y_z - Cc * x));  % Równanie stanu z regulatorem
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

% ---------- Regulacja LQR z wartością zadaną ----------
% Parametry regulacji
Q = eye(2);  % Penalizacja stanów
R = 0.1;     % Penalizacja sterowania

% Obliczenie macierzy wzmocnienia LQR
K = lqr(Ac, Bc, Q, R);

% Wartość zadana wyjścia
y_z = 1;

% Obliczenie x_ref i u_ref
x_ref = pinv(Cc) * y_z;  % Wartość odniesienia stanu
u_ref = -pinv(Bc) * (Ac * x_ref);  % Wartość odniesienia sterowania

% Równanie różniczkowe z regulacją LQR
odefun_lqr = @(t, x) Ac * x + Bc * (u_ref - K * (x - x_ref));

% Początkowe warunki
x0 = [0; 0];  % Stan początkowy

% Zakres czasu
tspan = [0 10];

% Rozwiązanie równań różniczkowych
[t, x_lqr] = ode45(odefun_lqr, tspan, x0);



% Obliczanie odpowiedzi wyjściowej
y_lqr = Cc * x_lqr';

% Rysowanie wykresu odpowiedzi
figure;
plot(t, y_lqr);
xlabel('Czas (s)');
ylabel('Odpowiedź wyjściowa y(t)');
title('Odpowiedź układu z regulatorem LQR');
grid on;