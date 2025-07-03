# ... (les commandes populate-demo-data et populate-new-data restent inchangées)
new_demo_products_data = [
    # Image 1: T-shirt rose GUCCI
    {
        'name': "T-shirt Gucci Rose Logo Pailleté", 'brand': "Gucci",
        'description': "Un t-shirt rose éclatant signé Gucci, rehaussé du logo emblématique en paillettes multicolores au dos. Confortable et chic pour une allure affirmée.",
        'price_info': "480€", 'image_file': "f1 (1).webp", 
        'tags': "gucci, t-shirt, rose, paillettes, logo, luxe, femme, mode", 'category': "Vêtements", 'gender': "Femme"
    },
    # Image 2: Montre chronographe argentée (type Swatch Irony)
    {
        'name': "Montre Chronographe Acier Classique", 'brand': "Swatch",
        'description': "Montre chronographe intemporelle avec bracelet et boîtier en acier inoxydable. Cadran noir contrastant, parfaite pour un style sportif et élégant.",
        'price_info': "175€", 'image_file': "f1 (2).webp", 
        'tags': "montre, chronographe, acier, sport, élégant, unisexe", 'category': "Montres", 'gender': "Unisexe"
    },
    # Image 3: Baskets Jordan 4 blanches et grises
    {
        'name': "Baskets Air Jordan 4 Rétro Blanches et Grises", 'brand': "Nike Air Jordan",
        'description': "Les iconiques Air Jordan 4 dans une palette de couleurs épurée blanche et grise, avec des touches de noir. Un must-have pour les passionnés de sneakers.",
        'price_info': "260€", 'image_file': "f1 (3).webp", 
        'tags': "nike, air jordan, jordan 4, sneakers, baskets, streetwear, basketball", 'category': "Chaussures", 'gender': "Unisexe"
    },
    # Image 4: Baskets de course noires et roses Nike
    {
        'name': "Baskets de Course Nike noires et roses", 'brand': "Nike",
        'description': "Baskets de course performantes et légères, idéales pour l'entraînement. Design dynamique noir avec logo et détails roses.",
        'price_info': "85€", 'image_file': "f1 (4).webp", 
        'tags': "nike, running, course, sport, baskets, femme, performance", 'category': "Chaussures", 'gender': "Femme"
    },
    # Image 5: T-shirt bleu col V uni
    {
        'name': "T-shirt Basique Bleu Col V", 'brand': "Essentiels Mode",
        'description': "Un t-shirt bleu uni à col V, simple et polyvalent. Tissu confortable pour un usage quotidien, facile à assortir.",
        'price_info': "28€", 'image_file': "f1 (5).webp", 
        'tags': "t-shirt, basique, col v, bleu, uni, confort, casual", 'category': "Vêtements", 'gender': "Unisexe"
    },
    # Image 6: T-shirt Halloween "Just waiting for Halloween"
    {
        'name': "T-shirt Imprimé 'Waiting for Halloween'", 'brand': "Spooky Style",
        'description': "T-shirt à message humoristique 'Just waiting for Halloween' avec un squelette relaxant. Parfait pour les amatrices de la saison effrayante.",
        'price_info': "32€", 'image_file': "f1 (6).webp", 
        'tags': "halloween, t-shirt, imprimé, fun, squelette, femme, décontracté", 'category': "Vêtements", 'gender': "Femme"
    },
    # Image 7: Polo turquoise homme
    {
        'name': "Polo Homme Turquoise Uni", 'brand': "Casual Wear",
        'description': "Polo de couleur turquoise vif pour homme, coupe classique et confortable. Idéal pour un look décontracté mais soigné.",
        'price_info': "48€", 'image_file': "f1 (7).webp", 
        'tags': "polo, homme, turquoise, uni, casual, été", 'category': "Vêtements", 'gender': "Homme"
    },
    # Image 8: Montre Casio digitale/analogique argentée
    {
        'name': "Montre Casio Vintage Ana-Digi Argent", 'brand': "Casio",
        'description': "Montre Casio au design rétro emblématique, combinant affichage analogique et numérique. Bracelet en acier inoxydable argenté.",
        'price_info': "60€", 'image_file': "f1 (8).webp", 
        'tags': "casio, montre, vintage, ana-digi, argenté, retro, unisexe", 'category': "Montres", 'gender': "Unisexe"
    },
    # Image 9: Baskets chaussettes noires Balenciaga
    {
        'name': "Baskets Montantes 'Speed' Balenciaga Noires", 'brand': "Balenciaga",
        'description': "Les célèbres baskets montantes 'Speed' de Balenciaga, style chaussette. Design épuré noir avec semelle sculptée blanche. Luxe et confort moderne.",
        'price_info': "Contacter pour prix", 'image_file': "f1 (9).webp", 
        'tags': "balenciaga, speed trainer, baskets, chaussettes, luxe, designer, noir, unisexe", 'category': "Chaussures", 'gender': "Unisexe"
    },
    # Image 10: Baskets Skechers noires et roses "Lightweight"
    {
        'name': "Baskets Skechers 'Lightweight Flex' Noires et Roses", 'brand': "Skechers",
        'description': "Baskets de sport Skechers légères et flexibles, idéales pour l'entraînement. Combinaison de noir et de rose vif pour un look dynamique.",
        'price_info': "68€", 'image_file': "f1 (10).webp", 
        'tags': "skechers, baskets, sport, femme, léger, flexibilité, training", 'category': "Chaussures", 'gender': "Femme"
    },
    # Image 11: Chaussures plates noires type babies "Prao"
    {
        'name': "Chaussures Babies en Cuir Noir 'Prao'", 'brand': "Prao",
        'description': "Élégantes chaussures plates de style babies en cuir noir de la marque Prao. Confortables pour un usage quotidien avec une touche classique.",
        'price_info': "95€", 'image_file': "f1 (11).webp", 
        'tags': "prao, chaussures plates, babies, cuir, noir, femme, confortable", 'category': "Chaussures", 'gender': "Femme"
    },
    # Image 12: Sandales compensées noires avec bride strass
    {
        'name': "Sandales Compensées Noires Bride Scintillante", 'brand': "Evening Sparkle",
        'description': "Sandales compensées en suédine noire avec une élégante bride cheville ornée de strass dorés. Parfaites pour ajouter une touche glamour à vos tenues.",
        'price_info': "78€", 'image_file': "f1 (12).webp", 
        'tags': "sandales, compensées, noir, strass, soirée, femme, chic", 'category': "Chaussures", 'gender': "Femme"
    },
    # Image 13: Sandales à talons fins noires Jimmy Choo
    {
        'name': "Sandales à Talons Aiguilles 'Lance' Jimmy Choo", 'brand': "Jimmy Choo",
        'description': "Les iconiques sandales 'Lance' de Jimmy Choo en cuir noir. Un design sophistiqué avec de multiples brides et un talon aiguille élégant.",
        'price_info': "Contacter pour prix", 'image_file': "f1 (13).webp", 
        'tags': "jimmy choo, sandales, talons hauts, luxe, designer, noir, femme, soirée", 'category': "Chaussures", 'gender': "Femme"
    },
    # Image 14: Escarpins peep-toe brillants avec ornements
    {
        'name': "Escarpins Peep-Toe Pailletés avec Bijoux", 'brand': "Glam Heels",
        'description': "Escarpins à plateforme et bout ouvert (peep-toe), recouverts de paillettes et ornés de bijoux en cristal sur l'empeigne. Pour une allure de star.",
        'price_info': "155€", 'image_file': "f1 (14).webp", 
        'tags': "escarpins, peep-toe, paillettes, strass, plateforme, soirée, femme, glamour", 'category': "Chaussures", 'gender': "Femme"
    },
    # Image 15: Chaussures de ville vernies noires homme "WIKILEAKS"
    {
        'name': "Chaussures de Ville Homme Vernies Noires", 'brand': "Wikileaks Footwear",
        'description': "Chaussures de ville élégantes pour homme en cuir verni noir brillant. Design moderne avec un détail métallique discret. Idéales pour les grandes occasions.",
        'price_info': "135€", 'image_file': "f1 (15).webp", 
        'tags': "wikileaks, chaussures de ville, homme, verni, noir, formel, élégant", 'category': "Chaussures", 'gender': "Homme"
    },
    # Image 16: Sac à main noir type cabas avec logo LV (Louis Vuitton)
    {
        'name': "Sac Cabas Louis Vuitton Cuir Embossé Noir", 'brand': "Louis Vuitton",
        'description': "Luxueux sac cabas Louis Vuitton en cuir noir finement embossé du monogramme. Spacieux et sophistiqué, avec des détails dorés.",
        'price_info': "Contacter pour prix", 'image_file': "f1 (16).webp", 
        'tags': "louis vuitton, sac à main, cabas, cuir embossé, luxe, femme, noir", 'category': "Sacs", 'gender': "Femme"
    },
    # Image 17: Sac cabas Louis Vuitton Neverfull Monogram
    {
        'name': "Sac Cabas Iconique Neverfull Monogram", 'brand': "Louis Vuitton",
        'description': "L'intemporel sac Neverfull de Louis Vuitton en toile Monogram classique, avec ses finitions en cuir naturel et sa pochette amovible.",
        'price_info': "Contacter pour prix", 'image_file': "f1 (17).webp", 
        'tags': "louis vuitton, neverfull, sac à main, cabas, monogram, toile, luxe, femme", 'category': "Sacs", 'gender': "Femme"
    },
    # Image 18: Sacoche bandoulière homme cuir noir
    {
        'name': "Sacoche Bandoulière Homme Cuir Noir Urbaine", 'brand': "City Leather Goods",
        'description': "Sacoche pratique pour homme en cuir noir grainé. Design compact avec multiples poches zippées, idéale pour un usage quotidien en ville.",
        'price_info': "88€", 'image_file': "f1 (18).webp", 
        'tags': "sacoche, bandoulière, homme, cuir, noir, pratique, ville", 'category': "Sacs", 'gender': "Homme"
    },
    # Image 19: Montre homme classique argentée OLEVS
    {
        'name': "Montre Homme OLEVS Acier Cadran Argenté", 'brand': "OLEVS",
        'description': "Montre OLEVS pour homme avec un design classique et élégant. Boîtier et bracelet en acier inoxydable, cadran argenté avec affichage date et jour, index en cristaux.",
        'price_info': "98€", 'image_file': "f1 (19).webp", 
        'tags': "olevs, montre, homme, classique, acier, argenté, date, business", 'category': "Montres", 'gender': "Homme"
    },
    # Image 20: Montre femme carrée or rose avec strass
    {
        'name': "Montre Femme Carrée Or Rose Cadran Noir", 'brand': "Rosy Timepieces",
        'description': "Montre féminine au boîtier carré tendance en finition or rose, avec une lunette sertie de cristaux. Cadran noir élégant et bracelet en métal or rose.",
        'price_info': "115€", 'image_file': "f1 (20).webp", 
        'tags': "montre, femme, or rose, carré, cristaux, tendance, bijou, cadran noir", 'category': "Montres", 'gender': "Femme"
    },
    # Image 21: Montre femme dorée fine Rmega (Longines-like)
    {
        'name': "Montre Femme Rmega Classique Dorée", 'brand': "Rmega",
        'description': "Montre femme d'une grande finesse par Rmega. Boîtier rond doré, cadran blanc épuré et bracelet milanais doré pour une élégance intemporelle.",
        'price_info': "240€", 'image_file': "f1 (21).webp", 
        'tags': "rmega, montre, femme, doré, classique, fin, élégant", 'category': "Montres", 'gender': "Femme"
    },
    # Image 22: Chemise à carreaux rouge et noire femme "dos"
    {
        'name': "Chemise à Carreaux Rouge et Noir Manches 3/4", 'brand': "DOS Fashion",
        'description': "Chemise à carreaux de style bûcheron en flanelle douce, coloris rouge et noir. Manches retroussables 3/4, coupe féminine décontractée.",
        'price_info': "42€", 'image_file': "f1 (22).webp", 
        'tags': "dos, chemise, carreaux, flanelle, rouge, noir, bûcheron, casual, femme", 'category': "Vêtements", 'gender': "Femme"
    },
    # Image 23: Robe de soirée longue bleue à volants
    {
        'name': "Robe de Gala Sirène Bleue Électrique", 'brand': "Red Carpet Dreams",
        'description': "Spectaculaire robe de soirée longue de style sirène, en satin bleu électrique. Bustier plissé et cascade de volants sur la jupe pour un impact maximal.",
        'price_info': "Contacter pour prix", 'image_file': "f1 (23).webp", 
        'tags': "robe de soirée, longue, sirène, bleu, volants, gala, événement, femme", 'category': "Vêtements", 'gender': "Femme"
    },
    # Image 24: Chemise homme noire cintrée avec détails blancs "THAILER"
    {
        'name': "Chemise Homme 'Thailer' Noire et Blanche", 'brand': "Thailer",
        'description': "Chemise homme Thailer à coupe cintrée, en noir profond avec des détails contrastants blancs au col et à la poche. Style moderne et affirmé.",
        'price_info': "69€", 'image_file': "f1 (24).webp", 
        'tags': "thailer, chemise, homme, cintrée, slim fit, noir, blanc, business, moderne", 'category': "Vêtements", 'gender': "Homme"
    },
    # Image 25: Pull homme noir col V avec chemise blanche en dessous (style)
    {
        'name': "Pull Homme Col V Profond et Chemise Superposée", 'brand': "Layered Look",
        'description': "Ensemble stylé pour homme : pull noir à col V profond en maille fine, porté sur une chemise blanche pour un effet de superposition chic et décontracté.",
        'price_info': "72€", 'image_file': "f1 (25).webp", 
        'tags': "pull, homme, col v, maille, noir, chic, superposition, chemise", 'category': "Vêtements", 'gender': "Homme"
    },
    # Image 26: Baskets Nike Air Max 90 bleu marine et blanc
    {
        'name': "Baskets Nike Air Max 90 Bleu Marine et Gris", 'brand': "Nike",
        'description': "Les classiques Nike Air Max 90 dans une combinaison de couleurs bleu marine, blanc et différentes teintes de gris. Un confort et un style qui traversent le temps.",
        'price_info': "145€", 'image_file': "f1 (26).webp", 
        'tags': "nike, air max, air max 90, sneakers, baskets, bleu marine, confort, streetwear", 'category': "Chaussures", 'gender': "Unisexe"
    },
    # Image 27: Sac à main Dior Lady Dior rose vif
    {
        'name': "Sac Iconique Lady Dior Cuir Rose Fuchsia", 'brand': "Dior",
        'description': "Le sac emblématique Lady Dior de la maison Dior, en cuir d'agneau rose fuchsia vibrant, avec le motif Cannage et les charms 'D.I.O.R.' argentés.",
        'price_info': "Contacter pour prix", 'image_file': "f1 (27).webp", 
        'tags': "dior, lady dior, sac à main, cuir, cannage, rose, fuchsia, luxe, femme, iconique", 'category': "Sacs", 'gender': "Femme"
    },
    # Image 28: Sac Louis Vuitton Pochette Métis Monogram (avec partie noire)
    {
        'name': "Sac Louis Vuitton Pochette Métis Bi-Matière", 'brand': "Louis Vuitton",
        'description': "Le sac Pochette Métis de Louis Vuitton revisité, combinant la toile Monogram classique avec des empiècements en cuir noir. Fermoir S-lock doré.",
        'price_info': "Contacter pour prix", 'image_file': "f1 (28).webp", 
        'tags': "louis vuitton, pochette metis, sac à main, monogram, cuir noir, bandoulière, luxe, femme", 'category': "Sacs", 'gender': "Femme"
    },
    # Image 29: Baskets roses type aquashoes/sport légères
    {
        'name': "Chaussures de Sport Aquatiques Roses Ultra-Légères", 'brand': "AquaFlex",
        'description': "Chaussures de sport roses spécialement conçues pour les activités aquatiques. Ultra-légères, respirantes et à séchage rapide.",
        'price_info': "38€", 'image_file': "f1 (29).webp", 
        'tags': "chaussures aquatiques, sport, léger, rose, femme, plage, séchage rapide", 'category': "Chaussures", 'gender': "Femme"
    },
    # Image 30: Escarpins roses à talons sculptés or
    {
        'name': "Escarpins de Conte de Fées Roses et Or", 'brand': "Enchanted Heels",
        'description': "Escarpins roses satinés dignes d'une princesse, avec un talon aiguille spectaculaire sculpté de motifs floraux en métal doré. Bout ouvert subtil.",
        'price_info': "Contacter pour prix", 'image_file': "f1 (30).webp", 
        'tags': "escarpins, soirée, rose, talon aiguille, sculpté, or, luxe, mariage, femme, conte de fées", 'category': "Chaussures", 'gender': "Femme"
    },
    # Image 31: Chaussures richelieu homme cuir marron clair (sur support transparent)
    {
        'name': "Chaussures Richelieu Homme Cuir Caramel Brogues", 'brand': "Artisan Crafted",
        'description': "Chaussures richelieu pour homme en cuir lisse couleur caramel, avec des perforations décoratives de style brogue. Un choix élégant pour le gentleman moderne.",
        'price_info': "185€", 'image_file': "f1 (31).webp", 
        'tags': "richelieu, oxford, homme, cuir, caramel, marron clair, brogue, formel, business", 'category': "Chaussures", 'gender': "Homme"
    },
    # Image 32: Chaussures de ville noires homme classiques (sur fond rouge)
    {
        'name': "Chaussures Oxford Homme Cuir Noir Brillant", 'brand': "Executive Class",
        'description': "Chaussures de ville de type Oxford en cuir noir brillant pour homme. Lignes épurées et laçage classique pour une élégance formelle irréprochable.",
        'price_info': "155€", 'image_file': "f1 (32).webp", 
        'tags': "chaussures de ville, oxford, homme, cuir, noir, brillant, classique, formel", 'category': "Chaussures", 'gender': "Homme"
    },
    # Image 33: Chaussures confort larges à scratch (avec insert)
    {
        'name': "Chaussons Thérapeutiques Extra-Larges à Velcro", 'brand': "OrthoComfort",
        'description': "Chaussons thérapeutiques conçus pour un confort maximal, avec une ouverture large et une fermeture par Velcro. Idéals pour les pieds larges, sensibles ou en convalescence.",
        'price_info': "79€", 'image_file': "f1 (33).webp", 
        'tags': "chaussures confort, chaussons, large, velcro, orthopédique, thérapeutique, unisexe", 'category': "Chaussures", 'gender': "Unisexe"
    },
    # Image 34: Sac Hermès Birkin orange
    {
        'name': "Sac Iconique Birkin Hermès Cuir Orange Vif", 'brand': "Hermès",
        'description': "Le légendaire sac Birkin d'Hermès en cuir de veau Togo couleur orange vif. Un symbole intemporel de luxe, d'artisanat et d'exclusivité.",
        'price_info': "Contacter pour prix (Extrêmement élevé)", 'image_file': "f1 (34).webp", 
        'tags': "hermès, birkin, sac à main, cuir, orange, luxe, iconique, femme, collection", 'category': "Sacs", 'gender': "Femme"
    },
    # Image 35: Sac à main femme cuir bordeaux structuré "VANDERWAH"
    {
        'name': "Sac à Main 'Vanderwah' Cuir Bordeaux Structuré", 'brand': "Vanderwah",
        'description': "Sac à main élégant et structuré 'Vanderwah' en cuir de couleur bordeaux. Design matelassé géométrique avec des pompons décoratifs et une bandoulière amovible.",
        'price_info': "125€", 'image_file': "f1 (35).webp", 
        'tags': "vanderwah, sac à main, cuir, bordeaux, structuré, chic, femme, pompon, matelassé", 'category': "Sacs", 'gender': "Femme"
    },
    # Image 36: Sac à main noir femme avec pompon fourrure "MIAMIN"
    {
        'name': "Sac à Main 'Miamin' Noir avec Pompon Fourrure", 'brand': "Miamin",
        'description': "Sac à main 'Miamin' de taille moyenne en simili-cuir noir texturé. Agrémenté d'un charmant pompon en fausse fourrure grise et de détails métalliques.",
        'price_info': "89€", 'image_file': "f1 (36).webp", 
        'tags': "miamin, sac à main, noir, pompon, fourrure, ville, femme, tendance", 'category': "Sacs", 'gender': "Femme"
    },
    # Image 37: Sacoche bandoulière homme cuir marron "ETROFERUTO" (différente de 18)
    {
        'name': "Sacoche Homme 'Etroferuto' Cuir Marron Foncé", 'brand': "Etroferuto",
        'description': "Sacoche bandoulière compacte 'Etroferuto' pour homme, en cuir marron foncé de qualité. Rabat frontal et multiples compartiments zippés.",
        'price_info': "92€", 'image_file': "f1 (37).webp", 
        'tags': "etroferuto, sacoche, bandoulière, homme, cuir, marron foncé, vintage", 'category': "Sacs", 'gender': "Homme"
    },
    # Image 38: Montre Audemars Piguet Royal Oak (gros plan)
    {
        'name': "Montre de Luxe Royal Oak Acier Cadran Bleu", 'brand': "Audemars Piguet",
        'description': "La prestigieuse montre Royal Oak d'Audemars Piguet. Boîtier et bracelet intégrés en acier inoxydable, lunette octogonale et cadran bleu avec motif 'Grande Tapisserie'.",
        'price_info': "Contacter pour prix (Extrêmement élevé)", 'image_file': "f1 (38).webp", 
        'tags': "audemars piguet, royal oak, montre, luxe, automatique, acier, bleu, homme, iconique", 'category': "Montres", 'gender': "Homme"
    },
    # Image 39: Montre Rolex Datejust Or Jaune et Diamants (vue de côté)
    {
        'name': "Montre Rolex Lady-Datejust Or Jaune Sertie", 'brand': "Rolex",
        'description': "Magnifique montre Rolex Lady-Datejust en or jaune 18 carats, avec une lunette et des index somptueusement sertis de diamants. Bracelet President emblématique.",
        'price_info': "Contacter pour prix (Extrêmement élevé)", 'image_file': "f1 (39).webp", 
        'tags': "rolex, datejust, lady-datejust, montre, or jaune, diamants, luxe, femme, joaillerie", 'category': "Montres", 'gender': "Femme"
    },
    # Image 40: Montre Jaeger-LeCoultre Reverso Duetto (vue de face)
    {
        'name': "Montre Jaeger-LeCoultre Reverso Classique Or Rose", 'brand': "Jaeger-LeCoultre",
        'description': "L'élégance intemporelle de la montre Reverso Classic Duetto par Jaeger-LeCoultre. Boîtier réversible en or rose serti de diamants, cadran argenté guilloché.",
        'price_info': "Contacter pour prix", 'image_file': "f1 (40).webp", 
        'tags': "jaeger-lecoultre, reverso, duetto, montre, or rose, diamants, luxe, femme, art déco", 'category': "Montres", 'gender': "Femme"
    },
    # Image 41: Tailleur pantalon rouge femme (modèle de face)
    {
        'name': "Ensemble Tailleur Femme Veste et Pantalon Rouge Vif", 'brand': "Signature Suits",
        'description': "Tailleur pantalon pour femme d'un rouge vif et affirmé. Veste cintrée à simple boutonnage et pantalon cigarette pour une silhouette moderne et puissante.",
        'price_info': "225€", 'image_file': "f1 (41).webp", 
        'tags': "tailleur, pantalon, femme, rouge vif, business, chic, élégant, moderne", 'category': "Vêtements", 'gender': "Femme"
    },
    # Image 42: Costume homme gris anthracite (modèle de face, ajustant sa veste)
    {
        'name': "Costume Homme Élégant Gris Foncé Coupe Ajustée", 'brand': "The Dapper Gent",
        'description': "Costume deux pièces pour homme en laine de qualité, couleur gris foncé. Coupe ajustée (slim fit) pour une allure contemporaine et sophistiquée.",
        'price_info': "460€", 'image_file': "f1 (42).webp", 
        'tags': "costume, homme, gris foncé, slim fit, business, formel, mariage, élégant", 'category': "Vêtements", 'gender': "Homme"
    },
    # Image 43: Baskets Skechers grises et roses (différentes de 10, plus claires)
    {
        'name': "Baskets Skechers 'Ultra Flex' Grises et Roses", 'brand': "Skechers",
        'description': "Baskets de sport Skechers 'Ultra Flex' pour femme, en maille chinée gris clair avec des touches de rose corail. Extrêmement légères et confortables.",
        'price_info': "72€", 'image_file': "f1 (43).webp", 
        'tags': "skechers, ultra flex, baskets, training, femme, gris clair, rose, confort, léger", 'category': "Chaussures", 'gender': "Femme"
    },
    # Image 44: Chaussures de randonnée Millet (vue latérale)
    {
        'name': "Chaussures de Trekking Millet Imperméables", 'brand': "Millet",
        'description': "Chaussures de trekking Millet robustes et imperméables, conçues pour les terrains difficiles. Offrent un excellent maintien et une bonne adhérence.",
        'price_info': "165€", 'image_file': "f1 (44).webp", 
        'tags': "millet, randonnée, trekking, montagne, imperméable, chaussures, outdoor, unisexe", 'category': "Chaussures", 'gender': "Unisexe"
    },
    # Image 45: Baskets Skechers roses à semelle épaisse (vue latérale)
    {
        'name': "Baskets Skechers 'Max Road 5' Roses", 'brand': "Skechers",
        'description': "Baskets de course Skechers 'Max Road 5' avec amorti maximal Hyper Burst. Tige en mesh rose respirant pour un confort et une performance optimisés.",
        'price_info': "95€", 'image_file': "f1 (45).webp", 
        'tags': "skechers, max road, baskets, running, femme, rose, confort, amorti, performance", 'category': "Chaussures", 'gender': "Femme"
    },
    # Image 46: Baskets Louis Vuitton blanches à monogramme (vue paire)
    {
        'name': "Paire de Baskets 'Time Out' Monogram LV", 'brand': "Louis Vuitton",
        'description': "Élégantes baskets de ville 'Time Out' signées Louis Vuitton, en cuir blanc rehaussé de la toile Monogram. Semelle extérieure en gomme gravée.",
        'price_info': "Contacter pour prix", 'image_file': "f1 (46).webp", 
        'tags': "louis vuitton, time out, sneakers, baskets, monogram, blanc, luxe, femme, paire", 'category': "Chaussures", 'gender': "Femme"
    },
    # Image 47: Gros plan baskets de course bleues (Brooks Glycerin? - Bout)
    {
        'name': "Baskets de Course Amorti Supérieur Bleu Orange", 'brand': "Performance Run",
        'description': "Baskets de course conçues pour un amorti supérieur et une foulée dynamique. Tige en mesh technique bleu avec détails orange vif.",
        'price_info': "148€", 'image_file': "f1 (47).webp", 
        'tags': "running, course, amorti, confort, baskets, sport, performance, bleu, orange", 'category': "Chaussures", 'gender': "Unisexe"
    },
    # Image 48: Sac de sport noir avec compartiment chaussures (vue différente)
    {
        'name': "Grand Sac de Sport Duffel Noir Multifonction", 'brand': "ActiveLife Gear",
        'description': "Grand sac de sport de type duffel en nylon résistant noir. Spacieux, avec de multiples poches et un compartiment ventilé pour chaussures ou affaires humides.",
        'price_info': "52€", 'image_file': "f1 (48).webp", 
        'tags': "sac de sport, duffel, voyage, fitness, gym, compartiment chaussures, noir, grand", 'category': "Sacs", 'gender': "Unisexe"
    },
    # Image 49: Montre Swatch Irony (identique à 2 - mais nouveau nom de fichier)
    {
        'name': "Montre Swatch Irony Chronographe Acier", 'brand': "Swatch",
        'description': "Montre chronographe Swatch Irony classique, boîtier et bracelet en acier inoxydable. Cadran noir épuré, un accessoire polyvalent.",
        'price_info': "178€", 'image_file': "f1 (49).webp", 
        'tags': "swatch, irony, montre, chronographe, acier, noir, unisexe", 'category': "Montres", 'gender': "Unisexe"
    },
    # Image 50: Montre Seiko Kinetic verte (vue de face)
    {
        'name': "Montre Homme Seiko Kinetic Cadran Vert Profond", 'brand': "Seiko",
        'description': "Montre Seiko Kinetic pour homme, alliant la précision du quartz à l'énergie du mouvement. Cadran vert profond et bracelet en cuir marron surpiqué.",
        'price_info': "285€", 'image_file': "f1 (50).webp", 
        'tags': "seiko, kinetic, montre, homme, vert, cuir, sport, élégant", 'category': "Montres", 'gender': "Homme"
    },
    # Image 51: Montre Casio femme cadran rose (vue rapprochée)
    {
        'name': "Montre Femme Casio Acier Cadran Rose Pastel", 'brand': "Casio",
        'description': "Montre Casio pour femme au design intemporel. Boîtier et bracelet en acier inoxydable, cadran rose pastel délicat avec affichage de la date et du jour.",
        'price_info': "62€", 'image_file': "f1 (51).webp", 
        'tags': "casio, montre, femme, rose pastel, acier, date, classique, quotidien", 'category': "Montres", 'gender': "Femme"
    },
    # Image 52: Polo bleu ciel (identique à 7 - mais nouveau nom de fichier)
    {
        'name': "Polo Homme Uni Bleu Ciel Classique", 'brand': "SkyBlue Basics",
        'description': "Polo classique pour homme en coton de couleur bleu ciel. Coupe confortable, idéal pour les loisirs ou une tenue décontractée.",
        'price_info': "38€", 'image_file': "f1 (52).webp", 
        'tags': "polo, homme, bleu ciel, uni, casual, coton", 'category': "Vêtements", 'gender': "Homme"
    },
    # Image 53: Baskets Air Jordan 1 Mid rouges et blanches (vue de profil)
    {
        'name': "Baskets Montantes Air Jordan 1 Mid Rouge/Blanc", 'brand': "Nike Air Jordan",
        'description': "Les emblématiques Air Jordan 1 Mid dans une combinaison de couleurs rouge et blanc audacieuse. Silhouette montante pour un style basketball affirmé.",
        'price_info': "195€", 'image_file': "f1 (53).webp", 
        'tags': "nike, air jordan, jordan 1, mid, sneakers, baskets, rouge, blanc, streetwear", 'category': "Chaussures", 'gender': "Unisexe"
    },
    # Image 54: T-shirt blanc Gucci Firenze (vue de face)
    {
        'name': "T-shirt Gucci 'Firenze 1921' Signature Blanc", 'brand': "Gucci",
        'description': "T-shirt blanc en coton doux signé Gucci, avec l'imprimé distinctif 'Firenze 1921' et la bande Web vert-rouge-vert. Un incontournable de la mode de luxe.",
        'price_info': "395€", 'image_file': "f1 (54).webp", 
        'tags': "gucci, t-shirt, blanc, firenze, logo, luxe, coton, mode, unisexe", 'category': "Vêtements", 'gender': "Unisexe"
    }
]