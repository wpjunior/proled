Zope SDE - Structured Document Editor

    SDE is a Zope-based editor for documents which present well defined structure, composed by sets of elements.

    SDE is XML oriented: the objects responsible for defining the structure of a document can be exported as a XML-Schema file (.xsd), and the document itself can be exported as a XML file, in raw format or rendered through XSLT files.

    SDE can be seen as a **tool for creating and editing XML documents based on a given XML-Schema definition**. The editor guides the user who is creating a document to produce a *valid* and *well-formed* XML document.

    How to Install? What are the Requirements?

        SDE is built upon the Zope OFS.OrderedFolder class, which is available since **Zope 2.7**.

        Unpack the SDE_x_x_x.tgz in the Products folder of your Zope instance, and restart it.

        Since all XSLT processing is made on the client-side (web browser!), use browser versions so up to date as possible. The best results are achieved on Mozilla, version 1.6 or newer.

    How to Use?

        In the ZMI (Zope Management Interface), you will be able to use two main types of objects, **SDE-Template** - to define a document type - and **SDE-Document** - to hold the document itself.

        "SDE-Document" objects can be seen as instances of "SDE-Template" objects.

        Obviously you can create several "SDE-Document" objects derived from the same "SDE-Template" object.

        This is the description for these two types of objects and its sub-objects:

__________

        - **SDE-Template**

            This is the object used to define documents templates. It is a folderish object (is able to contain other objects), and can hold "SDE-Template-Element" objects and "SDE-Template-Link" objects. The order (position) of these sub-objects contained in a SDE-Template IS relevant, and you can set it by checking the object(s) you want to move and clicking on "Up" or "Down" buttons in the ZMI.

            **Properties:**

            - Title

	        String - This is the standard "Title" property existing in many Zope Objects.

	    - xmlns_prefix

	        String - Defines the prefix used for the XML namespace when generating the XML-Schema. All XML documents created by SDE use XML namespaces. Here you define the prefix that will be present in every XML tag of your document, with the format &lt;xx:yyyyy&gt;, where xx is the xmlns_prefix, and yyyyy is the name of the element.

	    - xml_tag

	        String - Defines the name for the root tag of a XML document based on this template.

	    - default_xslt_for_html

	        String - Address (URL or relative path) for a XSLT file that will be used as default XSLT for transforming XML documents based on this template into HTML. Is used by the invocation of the document's method **renderXML** with a parameter "xsl=__default__".

	    - default_xslt_for_editor

	        String - Address (URL or relative path) for a XSLT file that will be used as default XSLT for editing  XML documents based on this template. Is used by the invocation of the document's method **renderXMLforEditing** with a parameter "xslt=__default__".

            **Methods:**

	    - *renderXSD*

	        Returns a XML-Schema file representing the structure defined in the template.

                Example of usage:: "http://your_server/your_template/renderXSD"

            **Sub-objects:**

            - **SDE-Template-Element**

	        This object is used to define an element in a document template. It's also a folderish object, and can contain others "SDE-Template-Element" objects, as well as "SDE-Templete-Link" and "SDE-Template-Attribute" objects.

	        A SDE-Template-Element is also able to hold some specific Python Scripts, that can be used as event-handlers (see below, at the "Events" section).

		Properties:

		    - *initial_text:* (text)

		        Default content for new instance of this element in a document. If left blank, the instance element will be created without any initial value;

		    - *optional:* (boolean)

		        Defines if the presence of an instance of this element in a document is or not optional. In the XSD rendered after its template, it produces the attribute "minOccurs='1'" when true, or "minOccurs='0'" when false;

		    - *multiple:* (boolean)

		        Defines if is possible to have more than one instance of this element in a document. It appears in the corresponding XSD as "maxOccurs='unbounded'" when true, or "maxOccurs='0'" when false;

		    - *has_own_value:* (boolean)

		        Indicates if the instance element can have a text value associated to it, or if it is only a grouping element that will hold other elements;

		    - *exclusivity_group* (int)

		  	The value of this attribute is meaningful when compared to the value of exclusivity_group of other elements at the same hierarchy level in the template. When two or more elements have the same value for exclusivity_group, it means that only one type of these elements can appear in the instance document. During the edition, after creating one instance of an element that has in its definition a given value for exclusivity_group, the editor will suppress the possibility for creating instances of elements that have in their definition the same value for exclusivity_group.

			The default value for this attribute is -1, what "turns off" this feature.

			In the corresponding XSD, a group of elements with the same value for exclusivity_group will be rendered inside a &lt;xs:choice&gt; &lt;/xs:choice&gt; structure;

		    - *xml_tag* (string)

		        Defines a XML tag name for instance elements that are instance of this definition. If not specified, the XML tag will be the same as the Zope id (converted to lowercase) for this definition object.

		    - *element_name* (string)

		        This is a label that can be presented by the Editor instead of the element's Zope id, what occurs if left blank.

		Methods:

		    - This object has no public methods.

		Events:

		    A SDE-Template-Element object can hold "Python Script" objects that can respond as event handlers to some situations during the document edition. These scripts, to be called automatically be the SDE, must have as "Zope id" one of the following names: "SDE_BeforeDelete", "SDE_AfterInsert" and "SDE_AfterMove".

		    - *SDE_BeforeDelete* (element)

		        This Python Script must have in its parameter list the parameter "element". "element" is the SDE-Document-Element object instance that is going to be deleted.

			It's invoked before the deletion, in a SDE-Document, of a SDE-Document-Element object corresponding to this SDE-Template-Element object.

		    - *SDE_AfterInsert* (element)

		        This Python Script must have in its parameter list the parameter "element". "element" is the SDE-Document-Element object instance that was created.

			It's invoked after the creation, in a SDE-Document, of a SDE-Document-Element object corresponding to this SDE-Template-Element object.

		    - *SDE_AfterMove* (element, direction)

		        This Python Script must have in its parameter list the parameters "element" and "direction". "element" is the SDE-Document-Element object instance that was moved, and direction is a string containing "UP" or "DOWN", indicating in which direction "element" was moved to.

			It's invoked after changing the position, in a SDE-Document, of a SDE-Document-Element object corresponding to this SDE-Template-Element object.

		**Sub-objects:**

		- **SDE-Template-Attribute**

		    This object defines an attribute for a SDE-Template-Element. It's rendered in a XSD as a &lt;xs:attribute&gt; tag, and appears as an element attribute when the document instance is rendered in XML.

		    Properties:

		        - *xsd_type* (list)

			    Defines the attribute's datatype.

			- *attribute_name*

			    This is a label that can be presented by the Editor instead of the attribute's Zope id, what occurs if left blank.

            - **SDE-Template-Link**

	        This object is used to create a link to a SDE-Template-Element. This is used in a template definition to avoid repeating the definition of elements that are necessary in more than one place in the template structure.

		Properties:

		    - *link_to* (string)

		        Contains a relative path to a SDE-Template-Element object. As in a filesystem path notation, it's possible to use ".." to indicate "parent", and "/" to separate object ids.

		    - *optional:* (boolean)

		        Look at SDE-Template-Element -> Properties -> optional

		    - *multiple:* (boolean)

		        Look at SDE-Template-Element -> Properties -> multiple

		    - *exclusivity_group:* (boolean)

		        Look at SDE-Template-Element -> Properties -> exclusivity_group

		Methods:

		    - This object has no public methods.

__________

        - **SDE-Document**

            This is the object used to contain a document. A document is ALWAYS based on a template (SDE-Template). Is the information contained in a template that allows the Editor to guide the user when editing a document.

            It is also a folderish object, and can hold only document elements ("SDE-Document-Element" objects). The order (position) of these elements IS relevant, and you can set it by checking the object(s) you want to move and clicking on "Up" or "Down" buttons in the ZMI.

	    Properties:

	        - *template_path:* (string)

		    It is the absolute Zope path (starting with "/" to represent Zope's root) for the Zope folder that contains the SDE-Template object used as template for this document instance;

		- *type:* (string)

		    This is the Zope "id" of the SDE-Template object used as template for this document instance;

		- *nextElemId:* (string)

		    This is an internal property, used by the Editor to sequentially create Zope ids for the elements contained in this document instance. The elements are created with ids SDE1, SDE2, SDE3, ...

            Methods:

	        - *renderXML* (xsl)

		    If no value is given for the 'xsl' parameter, renders the document in raw XML format. If the 'xsl' parameter is informed, the document is rendered using the XSLT file whose path and name is indicated in this parameter; If you call 'renderXML' with 'xsl=__default__' , the document will be rendered using the XSLT file indicated in the 'default_xslt_for_html' parameter defined in the template object.

		    URLs Examples:

			 'http://your_server/your_document/renderXML' -- renders the document in raw XML format.

			 'http://your_server/your_document/renderXML?xsl=__default__' -- renders the document using the XSLT file defined as default in its template.

			 'http://your_server/your_document/renderXML?xsl=/XSLT/Editor/pl.xsl' -- renders the document using the XSLT file located at /XSLT/Editor/pl.xsl

                    .

	        - *renderXMLforEditing* (action, p_id, p_path, p_type, p_pos, xslt)

                    The main inteface for editing documents with SDE is also built using XML and XSLT. The document is rendered by this method in a specific XML structure for edition, and there is a default XSLT file, SD_GenericEditor.xslt, which is used to render this XML and create the editor envinronment in HTML. So, you can fully customize the editor look&feel by creating your own XSLT file or by changing this default one.

		    This method, when called without parameters, renders the document in this specific XML format designed for the editor. Calling it with a parameter 'xslt=__default__' makes it return this XML linked to the XSLT file indicated in the 'default_xslt_for_editor' parameter defined in the template object (usually 'SD_GenericEditor.xslt').

		    This is also the method invoked to make changes in the document. The table below presents possible "Actions" and the necessary parameters for each action type. Please notice that "action" is also a parameter that has to be passed to this method with one of the possible values (in uppercase) presented below.

        	    |-------------------------------------------------------------------------------------------------------------------|
        	    |action   |parameters             | description                                                                     |
        	    |===================================================================================================================|
        	    |EDIT     | p_id                  | Renders the element whose id=p_id with the attribute "editing='yes'"            |
		    |         |                       | Using the XSLT SD_GenericEditor as interface, this element will appear as an    |
		    |         |                       | HTML textarea object, and the "save" option for it will be visible.             |
        	    |-------------------------------------------------------------------------------------------------------------------|
        	    |MOVE_UP  | p_path, p_id          | Move one position up the element identified by p_id located at p_path           |
        	    |-------------------------------------------------------------------------------------------------------------------|
        	    |MOVE_DOWN| p_path, p_id          | Move one position down the element identified by p_id located at p_path         |
        	    |-------------------------------------------------------------------------------------------------------------------|
        	    |CREATE   | p_path, p_type, p_pos | Creates, under the element p_path, a child of type p_type at the p_pos position |
        	    |-------------------------------------------------------------------------------------------------------------------|
        	    |DELETE   | p_path, p_id          | Removes the element identified by p_id located at p_path                        |
        	    |-------------------------------------------------------------------------------------------------------------------|
        	    |SAVE     | p_path, p_id, REQUEST | Saves the changes to the element p_id located at p_path                         |
		    |         |                       |                                                                                 |
        	    |         |                       | In the REQUEST object there shall be a form called 'form_edit' containing       |
        	    |         |                       | a object (textarea) called 'txa_text' and several objects (text) named          |
        	    |         |                       | tat_??????, where ?????? is an attribute name (sde_attr)                        |
        	    |-------------------------------------------------------------------------------------------------------------------|

		    URLs Examples:

			 'http://your_server/your_document/renderXMLforEditing' -- renders the document in a specific XML format for edition.

			 'http://your_server/your_document/renderXML?xslt=__default__' -- renders the document using the Editor XSLT file defined as default in its template.

	            .

                - *Validacao*

		    Nao me lembro cumé qui é.
