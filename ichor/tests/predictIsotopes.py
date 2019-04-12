from pyteomics.mass import mass

compo = mass.most_probable_isotopic_composition("C60H240O5")

print compo
print type(compo)


print mass.isotopic_composition_abundance(compo)