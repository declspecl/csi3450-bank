import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: 'index.html',
        banks: 'banks.html',
        loans: 'loans.html',
        people: 'people.html',
        transactions: 'transactions.html'
      }
    }
  }
});

