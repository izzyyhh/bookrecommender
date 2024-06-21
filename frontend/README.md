# Bookommender - Frontend

## Get Started

- `yarn` → Install dependencies
- `yarn dev` → Start development server
- `yarn build` → Build for production in /build dir

## Docker

- Just run `yarn start:docker` in the root directory of bookommender

### Dev

- `docker build -t bookommender-f -f .\Dockerfile.dev .`
- `docker run -p 3000:3000 bookommender-f`

### Production

- `docker build -t bookommender-f -f .\Dockerfile .`
- `docker run -p 3000:3000 bookommender-f-prod`
