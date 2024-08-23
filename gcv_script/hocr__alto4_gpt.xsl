<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:alto="http://www.loc.gov/standards/alto/ns-v4#"
                xmlns:hocr="http://www.example.org/hocr">
    
    <!-- Identity transformation -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- Root Element Transformation -->
    <xsl:template match="/hocr:html">
        <alto:alto xmlns:alto="http://www.loc.gov/standards/alto/ns-v4#"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="http://www.loc.gov/standards/alto/ns-v4# http://www.loc.gov/standards/alto/v4-2/alto.xsd">
            <alto:Description>
                <alto:MeasurementUnit>pixel</alto:MeasurementUnit>
            </alto:Description>
            <alto:Layout>
                <xsl:apply-templates select="//hocr:div"/>
            </alto:Layout>
        </alto:alto>
    </xsl:template>

    <!-- Page Transformation -->
    <xsl:template match="hocr:div">
        <alto:Page>
            <xsl:attribute name="ID"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:apply-templates select="hocr:span"/>
        </alto:Page>
    </xsl:template>

    <!-- TextBlock Transformation -->
    <xsl:template match="hocr:span">
        <alto:TextBlock>
            <xsl:attribute name="ID"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:attribute name="HPOS"><xsl:value-of select="@left"/></xsl:attribute>
            <xsl:attribute name="VPOS"><xsl:value-of select="@top"/></xsl:attribute>
            <xsl:attribute name="WIDTH"><xsl:value-of select="@width"/></xsl:attribute>
            <xsl:attribute name="HEIGHT"><xsl:value-of select="@height"/></xsl:attribute>
            <alto:TextLine>
                <xsl:apply-templates select="hocr:line"/>
            </alto:TextLine>
        </alto:TextBlock>
    </xsl:template>

    <!-- Line Transformation -->
    <xsl:template match="hocr:line">
        <alto:TextLine>
            <xsl:attribute name="ID"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:attribute name="HPOS"><xsl:value-of select="@left"/></xsl:attribute>
            <xsl:attribute name="VPOS"><xsl:value-of select="@top"/></xsl:attribute>
            <xsl:attribute name="WIDTH"><xsl:value-of select="@width"/></xsl:attribute>
            <xsl:attribute name="HEIGHT"><xsl:value-of select="@height"/></xsl:attribute>
            <alto:String>
                <xsl:value-of select="hocr:word"/>
            </alto:String>
        </alto:TextLine>
    </xsl:template>

</xsl:stylesheet>
