import { login, requestToken, getViews } from '../utils/utils';

const testView = (view, size) => {
  if (!view) {
    cy.log('Unexistent view');
    return;
  }
  cy.log(`View ${view.id}: ${view.name}`);
  cy.wrap(view).should('have.property', 'name');
  cy.wrap(view).should('have.property', 'id');
  cy.wrap(view).should('have.property', 'thumbnail');
  const { name, id } = view;
  context(`View ${name}`, () => {
    cy.visit(`/uif/view?id=${id}`);
    cy.get('.react-grid-item').should('exist');
    cy.document().toMatchImageSnapshot({
      threshold: 0.001,
      name: `${name} (${size})`,
    });
  });
};

describe('The user loads the available views', () => {
  let views, token, clear;

  before(() => {
    requestToken((t) => (token = t));
    getViews((v) => (views = v));
    clear = Cypress.LocalStorage.clear;
    Cypress.LocalStorage.clear = function () {
      return;
    };
    login();
});

  after(() => {
    Cypress.LocalStorage.clear = clear;
  });

  // Run at most 30 view tests
  // 375x812, 1280x800, 1440x900, 1920x1080
  ['iphone-x', 'macbook-13', [1440, 900], [1920, 1080]].forEach((size) => {
    context(`Testing screen size: ${size}`, () => {

      beforeEach(() => {
        if (Cypress._.isArray(size)) {
          cy.viewport(size[0], size[1]);
        } else {
          cy.viewport(size);
        }
      });

      Cypress._.range(0, 30).forEach((k) => {
        it(`View # ${k}`, () => {
          testView(views[k], size);
        });
      });
    });
  });
});
