package org.xmlon;

import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonToken;
import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;
import java.io.*;

/**
 * Streaming JSON to XON (XML Object Notation) converter.
 * 
 * This class converts JSON data to XON XML format in a streaming manner,
 * processing the JSON input incrementally without loading the entire
 * document into memory.
 * 
 * Implementation details:
 * - Uses Jackson's JsonParser which reads JSON token-by-token from the stream
 * - Uses StAX XMLStreamWriter which writes XML incrementally
 * - Only processes one JSON token at a time, keeping memory usage constant
 * - Can handle arbitrarily large JSON files without memory issues
 */
public class JsonToXonStreaming {
    
    private static final String XON_NAMESPACE = "https://xmlon.org/";
    private static final String XON_PREFIX = "xon";
    private static final String DEFAULT_ROOT_NAME = "json";
    
    private final JsonFactory jsonFactory;
    private final XMLOutputFactory xmlOutputFactory;
    
    public JsonToXonStreaming() {
        this.jsonFactory = new JsonFactory();
        this.xmlOutputFactory = XMLOutputFactory.newInstance();
    }
    
    /**
     * Convert JSON input stream to XON XML output stream.
     * 
     * @param jsonInput Input stream containing JSON data
     * @param xmlOutput Output stream for XON XML data
     * @param rootName Name for the root XML element (default: "json")
     * @throws IOException if there's an error reading JSON
     * @throws XMLStreamException if there's an error writing XML
     */
    public void convert(InputStream jsonInput, OutputStream xmlOutput, String rootName) 
            throws IOException, XMLStreamException {
        if (rootName == null || rootName.isEmpty()) {
            rootName = DEFAULT_ROOT_NAME;
        }
        
        // JsonParser reads token-by-token from the stream (true streaming, no full file load)
        // XMLStreamWriter writes incrementally to the output stream
        try (JsonParser parser = jsonFactory.createParser(jsonInput);
             OutputStreamWriter writer = new OutputStreamWriter(xmlOutput, "UTF-8")) {
            
            XMLStreamWriter xmlWriter = xmlOutputFactory.createXMLStreamWriter(writer);
            
            // Write XML declaration
            xmlWriter.writeStartDocument("UTF-8", "1.0");
            
            // Start root element
            JsonToken token = parser.nextToken();
            if (token == null) {
                throw new IOException("Empty JSON input");
            }
            
            // Determine root type and start element
            String rootType = getTypeForToken(token);
            xmlWriter.writeStartElement(rootName);
            xmlWriter.writeNamespace(XON_PREFIX, XON_NAMESPACE);
            xmlWriter.writeAttribute(XON_PREFIX, XON_NAMESPACE, "type", rootType);
            
            // Process root value
            processValue(parser, xmlWriter, token, rootType);
            
            // Close root element
            xmlWriter.writeEndElement();
            xmlWriter.writeEndDocument();
            xmlWriter.flush();
        }
    }
    
    /**
     * Convert JSON file to XON XML file.
     * 
     * @param jsonFile Path to input JSON file
     * @param xmlFile Path to output XON XML file
     * @param rootName Name for the root XML element
     * @throws IOException if there's an error reading/writing files
     * @throws XMLStreamException if there's an error writing XML
     */
    public void convertFile(String jsonFile, String xmlFile, String rootName) 
            throws IOException, XMLStreamException {
        try (FileInputStream jsonInput = new FileInputStream(jsonFile);
             FileOutputStream xmlOutput = new FileOutputStream(xmlFile)) {
            convert(jsonInput, xmlOutput, rootName);
        }
    }
    
    /**
     * Process a JSON value and write corresponding XML.
     */
    private void processValue(JsonParser parser, XMLStreamWriter xmlWriter, 
                             JsonToken currentToken, String currentType) 
            throws IOException, XMLStreamException {
        
        if (currentToken == JsonToken.START_OBJECT) {
            processObject(parser, xmlWriter);
        } else if (currentToken == JsonToken.START_ARRAY) {
            processArray(parser, xmlWriter);
        } else {
            // Primitive value
            String value = getValueAsString(parser, currentToken);
            if (value != null) {
                xmlWriter.writeCharacters(value);
            }
        }
    }
    
    /**
     * Process a JSON object.
     */
    private void processObject(JsonParser parser, XMLStreamWriter xmlWriter) 
            throws IOException, XMLStreamException {
        
        while (true) {
            JsonToken token = parser.nextToken();
            if (token == JsonToken.END_OBJECT) {
                break;
            }
            
            if (token != JsonToken.FIELD_NAME) {
                throw new IOException("Expected field name, got: " + token);
            }
            
            String fieldName = parser.getCurrentName();
            token = parser.nextToken();
            
            if (token == null) {
                throw new IOException("Unexpected end of JSON");
            }
            
            String type = getTypeForToken(token);
            String elementName = getElementName(fieldName);
            
            // Start element
            xmlWriter.writeStartElement(elementName);
            
            // Add xon:name attribute if field name is not valid XML element name
            if (!isValidXmlName(fieldName)) {
                xmlWriter.writeAttribute(XON_PREFIX, XON_NAMESPACE, "name", fieldName);
            }
            
            // Add type attribute
            xmlWriter.writeAttribute(XON_PREFIX, XON_NAMESPACE, "type", type);
            
            // Process value
            processValue(parser, xmlWriter, token, type);
            
            // End element
            xmlWriter.writeEndElement();
        }
    }
    
    /**
     * Process a JSON array.
     */
    private void processArray(JsonParser parser, XMLStreamWriter xmlWriter) 
            throws IOException, XMLStreamException {
        
        while (true) {
            JsonToken token = parser.nextToken();
            if (token == JsonToken.END_ARRAY) {
                break;
            }
            
            if (token == null) {
                throw new IOException("Unexpected end of JSON");
            }
            
            String type = getTypeForToken(token);
            
            // Start item element
            xmlWriter.writeStartElement("item");
            xmlWriter.writeAttribute(XON_PREFIX, XON_NAMESPACE, "type", type);
            
            // Process value
            processValue(parser, xmlWriter, token, type);
            
            // End item element
            xmlWriter.writeEndElement();
        }
    }
    
    /**
     * Get the XON type string for a JSON token.
     */
    private String getTypeForToken(JsonToken token) {
        if (token == null) {
            return "null";
        }
        
        switch (token) {
            case START_OBJECT:
                return "object";
            case START_ARRAY:
                return "array";
            case VALUE_STRING:
                return "string";
            case VALUE_NUMBER_INT:
            case VALUE_NUMBER_FLOAT:
                return "number";
            case VALUE_TRUE:
            case VALUE_FALSE:
                return "boolean";
            case VALUE_NULL:
                return "null";
            default:
                throw new IllegalArgumentException("Unexpected token type: " + token);
        }
    }
    
    /**
     * Get the value as a string for primitive types.
     */
    private String getValueAsString(JsonParser parser, JsonToken token) throws IOException {
        switch (token) {
            case VALUE_STRING:
                return parser.getText();
            case VALUE_NUMBER_INT:
            case VALUE_NUMBER_FLOAT:
                return parser.getText();
            case VALUE_TRUE:
                return "true";
            case VALUE_FALSE:
                return "false";
            case VALUE_NULL:
                return null;
            default:
                return null;
        }
    }
    
    /**
     * Get the XML element name for a field name.
     * Returns "prop" if the field name is not a valid XML element name.
     */
    private String getElementName(String fieldName) {
        if (isValidXmlName(fieldName)) {
            return fieldName;
        } else {
            return "prop";
        }
    }
    
    /**
     * Check if a string is a valid XML element name.
     * XML names must start with a letter or underscore, and contain only
     * letters, digits, underscores, hyphens, periods, and colons.
     */
    private boolean isValidXmlName(String name) {
        if (name == null || name.isEmpty()) {
            return false;
        }
        
        char first = name.charAt(0);
        if (!Character.isLetter(first) && first != '_') {
            return false;
        }
        
        for (int i = 1; i < name.length(); i++) {
            char c = name.charAt(i);
            if (!Character.isLetterOrDigit(c) && c != '_' && c != '-' && c != '.' && c != ':') {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * Main method for command-line usage.
     */
    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: JsonToXonStreaming <input.json> <output.xon.xml> [root_name]");
            System.exit(1);
        }
        
        String jsonFile = args[0];
        String xmlFile = args[1];
        String rootName = args.length > 2 ? args[2] : DEFAULT_ROOT_NAME;
        
        try {
            JsonToXonStreaming converter = new JsonToXonStreaming();
            converter.convertFile(jsonFile, xmlFile, rootName);
            System.out.println("Converted " + jsonFile + " to " + xmlFile);
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
