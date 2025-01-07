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

% Obliczanie odpowiedzi wyjściowej (y = Cx + Du)
y = Cc * x' + Dc * u;

% Rysowanie wykresu odpowiedzi skokowej
figure;
plot(t, y);
xlabel('Czas (s)');
ylabel('Odpowiedź skokowa y(t)');
title('Odpowiedź skokowa układu');
grid on;

% ---------- Regulacja Proporcjonalna ----------
y_z = 1;  % Wartość zadana
epsilon = y_z - y;  % Uchyb (różnica między wartością zadaną a rzeczywistą)
kp = 1;  % Wzmocnienie regulatora proporcjonalnego

% Regulacja (obliczanie nowego wejścia na podstawie uchybu)
u = kp * epsilon;
