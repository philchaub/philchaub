import os

def concat_files_in_folder(folder_path, output_file):
    try:
        # Ouvrir le fichier de sortie en mode écriture
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Parcourir les fichiers dans le dossier spécifié
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                name=filename.split(".")[0]
                
                # Vérifier si c'est un fichier et non un sous-dossier
                if os.path.isfile(file_path):
                    # Écrire le nom du fichier dans le fichier de sortie
                    outfile.write(f"\n--- Début du chapitre: {name} ---")
                    
                    
                    # Ouvrir le fichier pour lire son contenu
                    with open(file_path, 'r', encoding='utf-8') as infile:

                        while  content := infile.readline() :  
                            if any(x.isalpha() for x in content): outfile.write(content)

                    # Ajouter une séparation entre les fichiers
                    outfile.write(f"--- Fin du chapitre: {name} ---\n")
        
        print(f"Tous les fichiers ont été concaténés avec succès dans {output_file}")
    
    except Exception as e:
        print(f"Erreur lors de la concaténation des fichiers : {e}")

# Exemple d'utilisation
# Remplacez par le chemin réel du dossier
folder_path = "C:\\Users\\isisc\\IA\\cuda_rag\\cuda_rag\\Scripts\\blendercrew\\blender_doc\\parse_doc_\\"
output_file = "C:\\Users\\isisc\\IA\\cuda_rag\\cuda_rag\\Scripts\\ressource_documents\\blender_geometry_node_editor_doc.txt"    # Nom du fichier de sortie
concat_files_in_folder(folder_path, output_file)
