# Мониторинг

Данный дашборд предназначен для мониторинга производительности и стабильности ML-приложения в реальном времени. Он включает в себя метрики на инфраструктурном, реальном времени и прикладном уровнях, что позволяет отслеживать важные аспекты работы системы, такие как количество предсказаний, использование ресурсов и частоту HTTP-запросов.

## Для мониторинга выбраны метрики нескольких слоев:

### Инфраструткурный слой:
- **Использование виртуальной памяти**

Эта метрика выбрана, так как она показывает текущее использование памяти, что критично для производительности ML-приложений. Используется круговой график, потому что он наглядно отображает процентное соотношение использования ресурсов и позволяет быстро оценить текущее состояние.

### Метрики реального времени:
- **Рост количества предсказаний за минуту**

Эта метрика выбрана, так как она отображает динамику предсказаний, делая акцент на нагрузку на систему. Используется линейный график, потому что он позволяет отслеживать изменения во времени, а также выявлять пики и падения активности.

- **Частота HTTP-запросов (за минуту)**

Эта метрика выбрана для оценки нагрузки на сервер и определения возможных проблем с производительностью. Используется гистограмма, так как она помогает визуализировать распределение запросов во времени, что позволяет легко выявлять аномалии или часы пик.

### Метрики прикладного уровня:
- **Квантили предсказанных значений**

Эта метрика выбрана для оценки распределения предсказанных значений, что помогает понять, как модель ведет себя в разных условиях. Используются линейные графики для представления различных квантилей, так как они позволяют наглядно сравнить изменения во времени и выявить отклонения от нормы.

