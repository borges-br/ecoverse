export type FaqItem = {
  id: string;
  question: string;
  answer: string;
  category: string;
};

/** Answers describe the current delivery and partner workflow. */
export const FAQ_ITEMS: FaqItem[] = [
  {
    id: 'public-map', category: 'Pontos de coleta',
    question: 'Preciso de conta para consultar os pontos?',
    answer: 'O mapa é público. Você precisa de uma conta para registrar o descarte, gerar o QR e acompanhar a entrega.',
  },
  {
    id: 'accepted-materials', category: 'Descartes',
    question: 'Quais materiais posso descartar?',
    answer: 'Pilhas e baterias, eletrônicos, lâmpadas e óleo de cozinha. Confira no perfil do ponto quais tipos ele recebe e as condições de entrega.',
  },
  {
    id: 'point-materials', category: 'Pontos de coleta',
    question: 'Todos os pontos recebem os mesmos materiais?',
    answer: 'Não. Cada ponto informa os materiais aceitos, os horários e as orientações de recebimento. Consulte essas informações antes de levar seus itens.',
  },
  {
    id: 'find-point', category: 'Pontos de coleta',
    question: 'Como encontro um ponto de coleta?',
    answer: 'Abra Pontos, escolha o material e busque por cidade, bairro ou nome do local. Você também pode usar sua localização pelo botão do mapa. Confira o perfil do ponto antes de sair.',
  },
  {
    id: 'delivery', category: 'Descartes',
    question: 'Como faço a entrega?',
    answer: 'Toque no +, informe os materiais e escolha um ponto compatível. Revise o registro e apresente o QR ao chegar. O ponto confirma o recebimento depois da entrega.',
  },
  {
    id: 'home-pickup', category: 'Descartes',
    question: 'Vocês retiram os materiais na minha casa?',
    answer: 'Você leva os materiais até um ponto de coleta. Os operadores parceiros fazem a retirada dos pontos e organizam o transporte até a unidade de recebimento.',
  },
  {
    id: 'prepare', category: 'Descartes',
    question: 'Como preparo os materiais para entregar?',
    answer: 'Consulte o guia de materiais e as orientações do ponto escolhido. Verifique o tipo de material, a embalagem e os limites de quantidade ou tamanho aceitos pelo local.',
  },
  {
    id: 'quantities', category: 'Descartes',
    question: 'Como informo a quantidade?',
    answer: 'Pilhas e baterias, eletrônicos e lâmpadas são registrados em unidades inteiras. Para óleo de cozinha, informe o volume em litros, por exemplo: 1,5 L.',
  },
  {
    id: 'mixed-materials', category: 'Descartes',
    question: 'Posso colocar materiais diferentes no mesmo registro?',
    answer: 'Sim. Adicione os materiais e suas quantidades no cadastro. O ponto escolhido precisa aceitar todos os tipos incluídos. Se não houver um ponto compatível, faça registros separados.',
  },
  {
    id: 'cancel', category: 'Descartes',
    question: 'Posso cancelar um descarte?',
    answer: 'Sim, enquanto ele aguarda a entrega. Abra o registro em Descartes e use a opção de cancelamento. Depois que o ponto confirma o recebimento, essa ação deixa de ficar disponível.',
  },
  {
    id: 'find-qr', category: 'QR e rastreio',
    question: 'Onde encontro meu QR depois de registrar?',
    answer: 'Abra Descartes e selecione o registro. O QR fica no detalhe da entrega e pode ser ampliado para apresentar no ponto.',
  },
  {
    id: 'qr-confirmation', category: 'QR e rastreio',
    question: 'Gerar o QR já confirma minha entrega?',
    answer: 'Não. O QR identifica seu registro. O recebimento é confirmado pelo ponto quando você entrega os materiais.',
  },
  {
    id: 'tracking', category: 'QR e rastreio',
    question: 'O que consigo acompanhar depois da entrega?',
    answer: 'O recebimento no ponto, a retirada para transporte e a chegada à unidade parceira. As etapas aparecem no detalhe do descarte conforme os responsáveis atualizam a operação.',
  },
  {
    id: 'tracking-update', category: 'QR e rastreio',
    question: 'Meu descarte está sem atualização. O que faço?',
    answer: 'Confira o histórico no detalhe do registro. Se você já entregou os materiais e o recebimento ainda não aparece, consulte o ponto pelos contatos do perfil. As etapas de transporte são registradas pelos parceiros.',
  },
  {
    id: 'participation-points', category: 'Pontos e conquistas',
    question: 'Quando recebo os pontos de participação?',
    answer: 'Cada entrega EcoVerse confirmada pelo ponto gera 10 pontos de participação, creditados uma única vez. Criar um registro ou gerar o QR ainda não soma pontos.',
  },
  {
    id: 'achievements', category: 'Pontos e conquistas',
    question: 'Onde vejo meu nível e minhas conquistas?',
    answer: 'Abra Conta para consultar seu nível, os pontos acumulados e as conquistas. Os marcos consideram as entregas confirmadas e os critérios indicados em cada conquista.',
  },
  {
    id: 'profile', category: 'Conta',
    question: 'Como altero meus dados e minha foto?',
    answer: 'Abra Conta e toque em Editar perfil para alterar os dados de cadastro. Para trocar a foto, use o botão sobre o avatar. As opções de segurança ficam em Privacidade e segurança.',
  },
  {
    id: 'password', category: 'Conta',
    question: 'Esqueci minha senha. O que faço?',
    answer: 'Na tela de entrada, toque em Esqueci minha senha e informe o e-mail da conta. Siga as instruções recebidas e confira também a pasta de spam.',
  },
  {
    id: 'theme', category: 'Conta',
    question: 'Como mudo o tema do aplicativo?',
    answer: 'Abra Conta → Configurações e escolha Claro, Escuro ou Sistema. O tema claro é o padrão; sua escolha fica salva neste dispositivo.',
  },
  {
    id: 'operational-data', category: 'Privacidade',
    question: 'Quais informações os parceiros usam na operação?',
    answer: 'Os perfis autorizados consultam os dados necessários ao recebimento e ao transporte, como materiais, quantidades, código, etapas e ponto vinculado. Não inclua dados pessoais desnecessários nas observações da entrega.',
  },
  {
    id: 'close-account', category: 'Privacidade',
    question: 'Como encerro minha conta?',
    answer: 'Abra Conta → Privacidade e segurança e selecione o encerramento. Você pode exportar seus dados antes de confirmar. O processo anonimiza a conta e preserva o histórico operacional de rastreio.',
  },
];

const HOME_QUESTION_IDS = [
  'public-map', 'accepted-materials', 'point-materials', 'delivery', 'home-pickup',
  'quantities', 'find-qr', 'tracking', 'participation-points',
];
export const HOME_FAQ_ITEMS = HOME_QUESTION_IDS.map(id => FAQ_ITEMS.find(item => item.id === id)!);
export const FAQ_CATEGORIES = ['Todas', ...Array.from(new Set(FAQ_ITEMS.map(item => item.category)))];

export function normalizeFaqSearch(value: string) {
  return value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
}
