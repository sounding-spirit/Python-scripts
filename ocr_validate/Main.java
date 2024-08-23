import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.nio.file.Path;

import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;
import javax.xml.validation.Validator;

import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;

public class Main {
    // the name of the xsd file name which contains the alto schema
    private static String mXSDFileName = "alto-4-2.xsd";

    // main method that runs when program starts
    public static void main(String... args) throws URISyntaxException {
        // gets the resource path from args
        String path = args[0];
        System.out.println("Running ocr_validate on " + path); // can be commented
        File dir = new File(path);

        // gets the schema factory that will make the validator
        SchemaFactory factory = SchemaFactory.newInstance(
                "http://www.w3.org/2001/XMLSchema");
        // get the script directory path
        Path script_dir = Paths.get(Main.class.getProtectionDomain().getCodeSource().getLocation().toURI()).getParent();
        // get the xsd file
        File XSDFile = new File(Paths.get(script_dir.toString(), mXSDFileName).toString());

        try {
            // create a validator that checks the ocr files
            Schema schema = factory.newSchema(XSDFile);
            Validator validator = schema.newValidator();
            check(dir, validator);
        } catch (SAXException sch) {
            System.err.println("Error reading XML Schema: " + mXSDFileName);
            System.err.println(sch.getMessage());
            System.exit(ERROR_READING_SCHEMA);
        }
    }

    // gets into the director and check all files
    static void check(File dir, Validator validator) {
        for (File tmp : dir.listFiles()) {
            // if a file has the name ocr,
            // the parent folder is a target folder (containing images and ocr)
            if (tmp.getName().equals("ocr"))
                validate(dir, validator);
            // otherwise go inside the directories
            else if (tmp.isDirectory())
                check(tmp, validator);
        }
    }

    // check if all ocr files have a corresponding image,
    // and if all image files have a corresponding ocr
    // check if all ocr files are valid
    static void validate(File dir, Validator validator) {
        // get path to directories
        String path = dir.getAbsolutePath();
        System.out.println("\nGoing into folder " + path); // can be commented
        String path_ocr = Paths.get(path, "ocr").toString();
        File ocr_dir = new File(path_ocr);
        String path_img = Paths.get(path, "images").toString();
        File img_dir = new File(path_img);

        // list of ocr file names and image file names
        List<String> ocr_names = new ArrayList<>();
        List<String> img_names = new ArrayList<>();
        for (File f : ocr_dir.listFiles())
            ocr_names.add(f.getName().split("\\.")[0]);
        for (File f : img_dir.listFiles())
            img_names.add(f.getName().split("\\.")[0]);

        // check if all ocr files have coresponding image files
        for (String n : ocr_names)
            if (!img_names.contains(n))
                System.out.println(n + " does not have a corresponding image");
            else System.out.println(n + " has a corresponding image"); // can be commented

        // check if all image files have corresponding ocr files
        for (String n : img_names)
            if (!ocr_names.contains(n))
                System.out.println(n + " does not have a corresponding ocr");
            else System.out.println(n + " has a corresponding ocr"); // can be commented

        // validate against alto schema
        System.out.println();
        for (String n : ocr_names)
            validate(Paths.get(dir.getAbsolutePath(), "ocr", n + ".xml").toString(), validator);
    }

    // copied from
    // https://github.com/kba/xsd-validator/blob/master/src/xsdvalidator/validate.java

    private final static int VALIDATION_FAIL = 1;
    private final static int ERROR_READING_SCHEMA = 2;
    private final static int ERROR_READING_XML = 3;

    public static void validate(String mXMLFileName, Validator validator) {

        InputStream XMLFile = null;

        try {
            XMLFile = new FileInputStream(mXMLFileName);
        } catch (IOException e) {
            // if the ocr file cannot be found,
            // print error message
            e.printStackTrace();
            System.exit(1);
        }

        try {
            // if the validate method gives an error,
            // it is catched and the error message is printed out
            validator.validate(new StreamSource(XMLFile));
            // IMPORTANT: uncomment this line
            // if it is required to see which file validates
            System.out.println(mXMLFileName + " validates");
        } catch (SAXParseException ex) {
            System.out.println(mXMLFileName + " fails to validate because: \n");
            System.out.println(ex.getMessage());
            System.out.println("At: " + ex.getLineNumber()
                    + ":" + ex.getColumnNumber());
            System.out.println();
            // IMPORTANT: uncomment this line
            // if it is required to exit when a file does not validate
            // System.exit(VALIDATION_FAIL);
        } catch (SAXException ex) {
            System.out.println(mXMLFileName + " fails to validate because: \n");
            System.out.println(ex.getMessage());
            System.out.println();
            System.exit(VALIDATION_FAIL);
        } catch (IOException io) {
            System.err.println("Error reading XML source: " + mXMLFileName);
            System.err.println(io.getMessage());
            System.exit(ERROR_READING_XML);
        }
    }
}