// src/services/empresaRamoService.js — Mock
import { getCollection, setCollection, delay } from '../data/mockStore';

export const getRamosPorEmpresa = async (idEmpresa) => {
  await delay();
  const associacoes = getCollection('empresa_ramos').filter(
    (er) => er.id_empresa === Number(idEmpresa)
  );
  const ramos = getCollection('ramos');
  return associacoes
    .map((a) => ramos.find((r) => r.id === a.id_ramo))
    .filter(Boolean);
};

export const atrelarRamosAEmpresa = async (idEmpresa, idsRamo) => {
  await delay();
  const empresa_ramos = getCollection('empresa_ramos');
  const novas = idsRamo
    .filter((idRamo) => !empresa_ramos.some(
      (er) => er.id_empresa === Number(idEmpresa) && er.id_ramo === Number(idRamo)
    ))
    .map((idRamo) => ({ id_empresa: Number(idEmpresa), id_ramo: Number(idRamo) }));
  setCollection('empresa_ramos', [...empresa_ramos, ...novas]);
  return { message: `${novas.length} ramos atrelados com sucesso.` };
};

export const deleteAssociacao = async (idEmpresa, idRamo) => {
  await delay();
  const empresa_ramos = getCollection('empresa_ramos');
  setCollection(
    'empresa_ramos',
    empresa_ramos.filter(
      (er) => !(er.id_empresa === Number(idEmpresa) && er.id_ramo === Number(idRamo))
    )
  );
  return { message: 'Associação removida com sucesso.' };
};