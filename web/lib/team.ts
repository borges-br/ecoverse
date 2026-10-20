export type TeamMember = {
  id: string;
  name: string;
  photo: string;
  objectPosition: string;
  linkedin?: string;
  github?: string;
};

/** Current semester. Historical documents keep their original authorship. */
export const ECOVERSE_TEAM: TeamMember[] = [
  {
    id: 'nathan', name: 'Nathan Borges',
    photo: '/images/team/nathan-borges.png', objectPosition: '50% 25%',
    linkedin: 'https://www.linkedin.com/in/nathan-borges-ti/',
    github: 'https://github.com/borges-br/',
  },
  {
    id: 'vinicius', name: 'Vinícius Stadler Gorov',
    photo: '/images/team/ecoverse/vinicius-stadler-gorov.webp', objectPosition: '50% 32%',
  },
  {
    id: 'antonio', name: 'Antonio Carlos Damante de Souza',
    photo: '/images/team/ecoverse/antonio-carlos-damante-de-souza.webp', objectPosition: '50% 28%',
  },
  {
    id: 'guilherme', name: 'Guilherme Henrique de Assis Carvalho',
    photo: '/images/team/ecoverse/guilherme-henrique-de-assis-carvalho.webp', objectPosition: '50% 22%',
  },
  {
    id: 'lincoln', name: 'Lincoln Mariozzi Proença Sobrinho do Prado',
    photo: '/images/team/ecoverse/lincoln-mariozzi-proenca-sobrinho-do-prado.png', objectPosition: '50% 25%',
  },
  {
    id: 'matheus', name: 'Matheus Lisbôa Paludeto',
    photo: '/images/team/ecoverse/matheus-lisboa-paludeto.png', objectPosition: '52% 25%',
  },
];
