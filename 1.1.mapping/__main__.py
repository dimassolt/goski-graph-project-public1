# -*- coding: utf-8 -*-"""

import logging
import os, codecs

from argparse import ArgumentParser
from pathlib import Path

from pyrml.pyrml_mapper import RMLConverter 
from pyrml.functions import * 

from rdflib import Graph 

# Namespaces
parser = ArgumentParser()
parser.add_argument("-o", "--output", dest="output",
            help="Output file. If no choice is provided then standard output is assumed as default.", metavar="RDF out file")
parser.add_argument("-m", action="store_true", default=False,
            help="Enable conversion based on multiproccessing for fastening the computation.")
parser.add_argument("input", help="The input RML mapping file for enabling RDF conversion.")
parser.add_argument("ontology", help="The main ontology to create the generated KG.")
        
args = parser.parse_args()
logging.basicConfig(level=logging.DEBUG)
    
def execute_mapping():
    """
    Execute the mapping process using RML.
    This function reads the RML mapping file, converts it to RDF using the RMLConverter,
    and returns the generated RDF graph.
    """
    rml_converter = RMLConverter()
    g = rml_converter.convert(args.input) 
    return g

def store(g, output):    
    """
    Store the generated RDF graph in Turtle and N3 formats.
    This function takes the RDF graph and the output file path as arguments,
    and writes the graph to the specified file in both formats.
    """
    dest_folder = Path(output).parent
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
        
    with codecs.open(output + '.ttl', 'w', encoding='utf8') as out_file:
        out_file.write(g.serialize(format='turtle'))

    with codecs.open(output + '.n3', 'w', encoding='utf8') as out_file:
        out_file.write(g.serialize(format='nt'))

if __name__ == '__main__':
    
    g = execute_mapping()
    store(g, args.output)

    og = Graph()
    og.parse(args.ontology)

    for triple in g.triples((None, None, None)):
        og.add(triple)

    store(og, args.output + '_merged')
