# Jeu de donn?es d?mo

Contexte d'ex?cution: **conteneur backend**.

```bash
cd /home/frappe/frappe-bench
bench --site <site> execute datasets.demo.seed.run
```

Le seed est idempotent:

- cr?e un `Employee` de d?mo uniquement s'il n'existe pas d?j?
- ne supprime rien
