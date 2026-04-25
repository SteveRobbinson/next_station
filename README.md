# Next Station
Railway Exclusion Analysis

**Next Station** to aplikacja zaprojektowana do kwantyfikacji i wizualizacji zjawiska wykluczenia komunikacyjnego w Polsce. Projekt przetwarza dane przestrzenne, aby określić dostępność infrastruktury kolejowej dla każdej lokalizacji w kraju.

### Kluczowe funkcjonalności:
* **Dynamiczne Heatmapy Wykluczenia:** Generowanie map ciepła ilustrujących natężenie wykluczenia komunikacyjnego w skali całego kraju.
* **Ranking Deficytów Infrastrukturalnych:** Automatyczna identyfikacja 10 obszarów o najniższym poziomie dostępności.
* **Symulacje Impact Analysis:** Symulacje, pozwalające na wirtualne rozmieszczenie nowych stacji kolejowych i oszacowanie liczby osób zyskujących dostęp do komunikacji.<br>

---

<h3 align="center">Architecture & Data Flow</h3>

---

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="images/dark-theme.svg">
  <source media="(prefers-color-scheme: light)" srcset="images/light-theme.svg">
  <img alt="Ingestion Pipeline Architecture" src="images/schemat.svg">
</picture>
