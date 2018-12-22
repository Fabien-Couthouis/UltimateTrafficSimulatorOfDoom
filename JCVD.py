#!/usr/bin/env python
# coding: utf-8

from random import *

JCVD={
0:"Quand on sort d'un placenta à l'age de 42 ans et quand on a l'intelligence, le brain, le computer, la mémoire d'un 40 ans mais qui est vide, elle doit se remplir de jour en jour, elle doit sponging, elle doit elle doit prendre comme une éponge, elle doit elle doit... ok ?",
1:"Moi, Adam et Eve, j’y crois plus tu vois, parce que je suis pas un idiot : la pomme ça peut pas être mauvais, c’est plein de pectine…",
2:"Une noisette, j'la casse entre mes fesses tu vois... ",
3:"Je crois au moment. S'il n'y a pas le moment, à ce moment-là, il faut arriver a ce moment-là, au moment qu'on veut",
4:"J'adore les cacahuètes. Tu bois une bière et tu en as marre du gout. Alors tu manges des cacahuètes. Les cacahuètes c'est doux et salé, fort et tendre,comme une femme. Manger des cacahuètes, it's a really strong feeling. Et après tu as de nouveau envie de boire de la bière. Les cacahuètes c'est le mouvement perpétuel à la portée de l'homme",
5:"Selon les statistiques, il y a une personne sur cinq qui est déséquilibrée. S'il y a 4 personnes autour de toi et qu'elles te semblent normales, c'est pas bon.",
6:"Je suis fascine par l'air. Si on enlevait l'air du ciel, tous les oiseaux tomberaient par terre....Et les avions aussi.... En même temps l'air tu peux pas le toucher...ça existe et ça existe pas...Ça nourrit l'homme sans qu'il ait faim...It's magic...L'air c'est beau en même temps tu peux pas le voir, c'est doux et tu peux pas le toucher.....L'air c'est un peu comme mon cerveau...",
7:"Le monde est composé de flèches et de molécules, et d'électricité,comme le Big-Bang tu vois, et tout ça ensemble, ça forme l'Univers.",
8:"Mes autres prénoms sont Camille et François. J'aime bien Camille, non ? Ça fait 'old fashion', tu trouves pas ? Ça respire le meuble de Provence !",
9:"Si tu travailles avec un marteau-piqueur pendant un tremblement de terre, désynchronise-toi, sinon tu travailles pour rien.",
10:"Une femme qui est enceinte, par exemple, elle est aware qu'elle attend un enfant...",
11:"Nous les humains, on a inventé le temps. Mais le temps n'existe pas, car il y a une matter, une puissance de compression, qui n'est pas la même pour chaque species on earth.",
12:"Une vache, ça te bouffe trois hectares, moi, avec trois hectares, je te fais deux mille kilos de riz... avec trois hectares, je te nourris Avignon, tu vois...",
13:"La vie c'est quelque chose de tres fort et de tres beau.... La vie appartient a tous les vivants. It's both a dream and a feeling. C'est etre ce que nous ne sommes pas sans le rester. La vie c'est mourir aussi....Et mourir c'est vraiment strong...c'est rester en vie au dela de la mort...Tous ceux qui sont morts n'ignorent pas de le savoir",
14:"Quand tu prends confiance en la confiance tu deviens confiant.",
15:"Y'a pas de religions mon frère. On est aware.",
16:"L'être humain, en général, dans la vie, réacte. On réacte, c'est à dire qu'on fait ce qu'on est supposé faire. Travailler, manger... J'm'excuse de l'expression; chier, mais je trouve qu'un être humain doit créer.",
17:"Quand tu joues au Go.. faut être aware. Si t'es pas aware, tes pierres sont mortes, et toi avec.",
18:"La drogue, c'est comme quand tu close your eyes et que tu traverses la rue.",
19:"Je crois en Dieu....... un plus un égale un. Y'a Jean-Claude, y'a Dieu, dans le même corps. Si on peut s'unifier, on devient ce qu'on appelle les miracles, et chaque personne a le seigneur en soi. We're all one. Je crois VRAIMENT en Seigneur."
}


def randomPhrase(dic):
	return dic[randint(0,len(dic))]


